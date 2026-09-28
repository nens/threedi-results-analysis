# Result loading and layer isolation

This describes how computational grids and simulation results get loaded into QGIS, and how the resulting layers are organized in the layer tree depending on the loading mode. It separates the common result-opening pipeline from the mode-specific layer placement and ownership rules.

Read this together with `threedi_plugin.py`, `threedi_plugin_model_validation.py` and `threedi_plugin_layer_manager.py`.

## Overview

Loading a result always goes through the same three collaborators, in the same order:

```mermaid
sequenceDiagram
    participant Caller as ThreeDiPlugin.load_result()
    participant Validator as ThreeDiPluginModelValidator
    participant Loader as ThreeDiPluginLayerManager
    participant Model as ThreeDiPluginModel

    Caller->>Validator: validate_result_grid(result_path, grid_path, project, layer_path)
    Validator->>Validator: validate_grid(...) — find-or-create the grid
    Validator-->>Loader: grid_valid(grid_item, project)
    Loader->>Loader: load_grid(grid_item, project)
    Loader-->>Model: grid_loaded(grid_item)
    Model->>Model: add_grid() emits grid_added
    Validator->>Validator: _validate_result(...) — validate the result file
    Validator-->>Loader: result_valid(result_item, grid_item)
    Loader->>Loader: load_result(result_item, grid_item)
    Loader-->>Model: result_loaded(result_item, grid_item)
    Model->>Model: add_result() emits result_added
```

`ThreeDiPluginModel` is the source of truth for *what* is loaded (one `ThreeDiGridItem` per computational grid, with `ThreeDiResultItem` children). `ThreeDiPluginLayerManager` is the source of truth for *which QGIS layers* represent that state, and owns their lifecycle.

Two optional keyword arguments change how the QGIS layer tree is organized, without changing the model tree: `project` (for grouping results per project) and `layer_path` (for placing isolated result layers at a source-derived path).

> [!IMPORTANT]
> `project` and `layer_path` only affect the organization and ownership of layers in the layer panel, not the results analysis dock widget. This gives three loading modes.

## How a result is opened

The three modes below use the same loading pipeline. The mode only changes
where the resulting QGIS layers are placed and who owns them; it does not
change how the result datasource is opened.

1. `validate_grid()` finds an existing `ThreeDiGridItem` or creates one for
   the computational grid. A new grid normally causes `load_grid()` to convert
   the `.h5` gridadmin to a `.gpkg` (if needed) and copy its tables into QGIS
   layers.
2. `validate_result_grid()` validates the result file and creates a
   `ThreeDiResultItem` linked to the matching grid item.
3. `load_result()` prepares the result datasource through the established
   `ThreeDiResultItem.threedi_result` path and adds the dynamic
   `result_...`/`initial_value_...` fields to the layers owned by that result.
4. The model records the grid and result, and emits the normal model signals.
   Tools use those signals and the result's layer accessors rather than
   discovering result layers independently.

The computational-grid conversion is shared: results using the same grid do
not convert the gridadmin repeatedly. The layer manager also handles
waterdepth rasters, styling, cleanup, and project persistence using the same
ownership rules described below.

When a grid is first requested only by an isolated result, creation of the
grid-owned shared layers is deferred. The isolated result gets its own layers
immediately. If a standalone or project-based result later uses that same
grid, the shared grid layers are materialized on demand. See
`Deferred grid-layer creation` below.

## Loading modes

The modes differ in layer placement and ownership, not in the result-opening
pipeline above.

### Mode 1: standalone (no `project`, no `layer_path`)

This is the mode used by the Results Analysis result-manager UI itself.

The result uses the grid's shared QGIS layers. `ThreeDiResultItem.layer_path`
is `None`, and its dynamic fields are added to `ThreeDiGridItem.layer_ids`.
Waterdepth and tool groups are also attached to the grid's `layer_group`, so
multiple results using one grid share those layer containers.

Concretely, if Result A and Result B are both loaded against the same
computational grid, **both show up under this exact same `<grid name>`
group** — QGIS never gets a second, separate group for Result B. Then if a Result C was added for another grid, a new group is added:

```text
gridadmin foo/
├── Computational grid/          # shared by all results for the same model
├── Waterdepth/                  # shared group; one raster layer per result that has one
    ├── max wd result-a
    └── max wd result-b
└── Statistics/                  # shared group; one subgroup per result that used the tool
    └── result-a/
        └── ...
gridadmin bar/
├── Computational grid/
├── Waterdepth/layer per result that has one
    └── max wd result-c
└── Statistics/ per result that used the tool
    └── result-c/
        └── ...
```


### Mode 2: project-based (`project` keyword)

The layer tree gains one extra wrapper level compared to mode 1; layer ownership (including `Waterdepth` and the tool groups) is otherwise identical.

So if for the previous example the results for gridadmin foo and bar are in different projects, the tree looks like

```text
project foo/
   └── gridadmin foo/
       ├── Computational grid/
       └──  Waterdepth/
           ├── max wd result-a
           └── max wd result-b
project bar/
   └── gridadmin bar/
       ├── Computational grid/
       └──  Waterdepth/
           └── max wd result-c
```

But if Result A and Result B are in different projects, the three looks like:
```text
project foo/
   └── gridadmin foo/
       ├── Computational grid/
       └──  Waterdepth/
           └── max wd result-a
project bar/
   └── gridadmin foo/
       ├── Computational grid/
       └──  Waterdepth/
           └── max wd result-c  b
```


### Mode 3: isolated layers (`layer_path` keyword)

Used by the current Rana integration, which knows the ordered file-tree
location a result came from (e.g. `["<project>", "files", "folder", "result.zip"]`) and wants the QGIS layer tree to mirror it.

> [!NOTE]
> a non-empty `layer_path` always takes precedence over `project`, even if both are supplied.

Unlike modes 1 and 2, an isolated result does **not** reuse the grid's shared layers. `ThreeDiPluginLayerManager.load_result()` copies fresh, independent vector-layer instances from the same underlying GeoPackage into the result's *own* layer group (`ThreeDiResultItem.layer_group` and `ThreeDiResultItem.layer_ids`). This lets two results that share one computational grid (same schematisation revision, different result files) have independent visibility, styling, aliases, fields and cleanup. The underlying `.gpkg` conversion is still only performed once and reused. The `ThreeDiGridItem` itself is *not* duplicated: the Results Analysis model still keeps one logical grid item per computational grid, and multiple isolated results (with different `layer_path` values) can be children of the same grid item. Only the *QGIS layers* differ per result; the *model* tree looks the same as in the other modes.

In isolated mode, each ThreeDiResultItem stores its layer_path, its result-owned layer_group, and its result-owned layer_ids. The result remains a child of the matching ThreeDiGridItem in the Results Analysis model, but its QGIS layers are tracked independently from the grid. In non-isolated modes these result-owned attributes remain unused: the result uses its parent grid’s layer_group and layer_ids instead. This lets the model retain the link between a result and its computational grid while allowing isolated results to appear at separate locations in the QGIS layer tree.

For two results, `result-a.zip` and `result-b.zip`, that share the same computational grid, the model tree looks like this:

```text
project foo/
    └── files
    ├── result-a.zip/
        └── Computational grid/
        └── Waterdepth/
            └── max wd result-a
    └── result-b.zip/
        └── Computational grid/
        └── Waterdepth/
            └── max wd result-b
```


## Deferred grid-layer creation

To avoid this duplicate creation of computational grid layers, `ThreeDiGridItem` has a one-shot hint,
`defer_layer_creation`:

```mermaid
flowchart TD
    A["validate_grid(..., layer_path=[...])"] -->|"grid is genuinely new"| B["new_grid.defer_layer_creation = bool(layer_path)"]
    B --> C["grid_valid.emit(new_grid, project)"]
    C --> D["load_grid(new_grid, project)"]
    D --> E{"defer_layer_creation?"}
    E -->|"True"| F["clear the flag, grid_loaded.emit(new_grid)\n(model registers the grid; no 'Computational grid' layers yet)"]
    E -->|"False"| G["create the grid's own layers as usual"]
```

So a grid requested purely for isolated results is registered in the model (`model.add_grid()` still fires, and all the usual `grid_added` listeners still run), but `ThreeDiGridItem.layer_group` stays `None` and `ThreeDiGridItem.layer_ids` stays empty until (and unless) something that actually needs the shared layers comes along.

That "something" is a non-isolated (standalone or project-based) result attaching to the same grid later — which can happen because grids are matched and reused across loads by their model slug. `load_result()` lazily creates the grid's own layers on demand the first time this happens:

```mermaid
flowchart TD
    A["load_result(result_item, grid_item)"] --> B{"result_item.layer_path?"}
    B -->|"yes"| C["create/reuse the result's own independent layers"]
    B -->|"no"| D{"grid_item.layer_group is None\nand not grid_item.layer_ids?"}
    D -->|"yes (still deferred)"| E["materialize the grid's own layers now\n(_add_layers_from_gpkg), exactly as\nload_grid() would have done eagerly"]
    D -->|"no (already exist)"| F["reuse the existing grid-owned layers"]
    C --> G["add this result's fields to its owning layer(s)"]
    E --> G
    F --> G
```

The extra `not grid_item.layer_ids` check (in addition to `layer_group is None`) matters for tests/tools that construct a `ThreeDiGridItem` with `layer_ids` populated directly without bothering to set up a real `layer_group`: only a grid with *neither* signal set is considered
"genuinely deferred and not yet materialized".

Because deferral only ever *postpones* eager creation and materialization  is idempotent (a second standalone result attaching later just reuses the  already-created layers), the two possible attachment orders for one grid  converge on the same end state:

- **isolated result first, standalone result later**: grid stays empty until the standalone result attaches, then its layers are created on demand.
- **standalone result first, isolated result later**: the grid's layers are created immediately as before; the isolated result's independent layers are unaffected either way.

`unload_grid()` and `update_grid()` tolerate a grid that never materialized its own layers (nothing to remove/rename) instead of asserting.

## Project save and load (XML persistence)

The RA model and its layer ownership are persisted inside the QGIS project file itself, as a custom `<threediPluginModel>` element. Saving and loading a project goes through `ThreeDiPlugin`, wired to three `QgsProject` signals:

```mermaid
sequenceDiagram
    participant QGIS as QgsProject
    participant Plugin as ThreeDiPlugin
    participant Serializer as ThreeDiPluginModelSerializer

    Note over QGIS,Serializer: Saving
    QGIS->>Plugin: writeProject(doc)
    Plugin->>Serializer: write(model, doc, resolver)
    Serializer-->>Plugin: <threediPluginModel> tree + <tools> node
    Plugin->>Plugin: each tool writes into <tools>
    QGIS->>Plugin: writeMapLayer(layer, elem, doc)  # once per QGIS layer
    Plugin->>Serializer: remove_result_field_references(elem, field_names)

    Note over QGIS,Serializer: Reopening
    QGIS->>Plugin: readProject(doc)
    Plugin->>Plugin: model.clear()
    Plugin->>Serializer: read(loader, doc, resolver)
    Serializer->>Plugin: loader.load_grid(...) / loader.load_result(...) per node
    Plugin->>Plugin: each tool reads from <tools>
```

### XML shape

```xml
<qgis>
  ...
  <threediPluginModel>
    <grid path="..." text="..." id="..." project="...(mode 2 only)">
      <layer id="..." table_name="node"/>
      <layer id="..." table_name="flowline"/>
      ...
      <result path="..." text="..." id="..." check_state="2"
              layer_path="...(mode 3 only)">
        <layer id="..." table_name="node"/>   <!-- mode 3 only -->
        ...
      </result>
      ...
    </grid>
    ...
    <tools>...</tools>  <!-- each tool's own persisted state -->
  </threediPluginModel>
</qgis>
```

`<grid>` and `<result>` each get a stable, persisted `id` (tracked in `already_used_ids` to avoid collisions across reopen/re-add) that downstream tools use to correlate their own persisted state (in `<tools>`) back to the right model node. `check_state` records whether the result was
checked (visible/animated) when saved.

Continuing the `gridadmin` / `result-a.zip` / `result-b.zip` example from above, here is what actually gets written for each mode (abbreviated, `<layer>` children of `<grid>`/`<result>` shown for `node` only):

**Mode 1: standalone** — no `project`, results carry no `layer_path` and no `<layer>` children of their own (they use the grid's):

```xml
<grid path="gridadmin.gpkg" text="gridadmin" id="g1">
  <layer id="node_layer_id" table_name="node"/>
  <result path="result-a.zip/results_3di.nc" text="result-a.zip" id="r1" check_state="2"/>
  <result path="result-b.zip/results_3di.nc" text="result-b.zip" id="r2" check_state="2"/>
</grid>
```

**Mode 2: project-based** — identical, plus the `project` attribute on
`<grid>`:

```xml
<grid path="gridadmin.gpkg" text="gridadmin" id="g1" project="my-organisation">
  <layer id="node_layer_id" table_name="node"/>
  <result path="result-a.zip/results_3di.nc" text="result-a.zip" id="r1" check_state="2"/>
  <result path="result-b.zip/results_3di.nc" text="result-b.zip" id="r2" check_state="2"/>
</grid>
```

**Mode 3: isolated** — each `<result>` carries its own `layer_path` (joined
with `/`, since it is a display path, not a filesystem path — see below)
and its own `<layer>` children. If this grid was never used by a
non-isolated result in the saved session, its own `<layer>` children are
simply absent (see "Deferred layers on restore" below):

```xml
<grid path="gridadmin.gpkg" text="gridadmin" id="g1">
  <result path="result-a.zip/results_3di.nc" text="result-a.zip" id="r1" check_state="2"
          layer_path="my-model/revision-1/result-a.zip">
    <layer id="result_a_node_layer_id" table_name="node"/>
  </result>
  <result path="result-b.zip/results_3di.nc" text="result-b.zip" id="r2" check_state="2"
          layer_path="my-model/revision-1/result-b.zip">
    <layer id="result_b_node_layer_id" table_name="node"/>
  </result>
</grid>
```

### Path resolution

`path` attributes (grid and result file paths) are converted through
`QgsPathResolver` in `ThreeDiPlugin.write()`/`read()`:

- If the QGIS project's own path storage is set to relative
  (`QgsProject.filePathStorage() == Qgis.FilePathType.Relative`), the
  resolver is built with the project's file name, so `path` is written
  relative to the project file and resolved back to an absolute path on
  read.
- Otherwise, `path` is written and read as an absolute path.

`layer_path` is **not** a filesystem path and is never passed through the
resolver: it is a plain, already-serializable list of display-name
components (see the earlier "Serialize `layer_path` as a display path"
rationale — components must not themselves contain `/`), joined with `/`
for storage and split back into a list on read.

### Dynamic result fields are not persisted directly

The `result_...`/`initial_value_...` fields that `load_result()` adds to a
layer include a random UUID in their name (see
`ThreeDiPluginLayerManager.load_result`), so they cannot be meaningfully
reused across a save/reopen cycle. Instead of persisting them:

- `ThreeDiPlugin.write_map_layer()` (connected to `writeMapLayer`, called by
  QGIS once per map layer, right after `write()`) strips any reference to
  the *current* session's dynamic field names from that layer's own
  `<maplayer>` XML element — its datasource query string, field
  configuration, aliases, defaults and constraints
  (`ThreeDiPluginModelSerializer.remove_result_field_references`). It looks
  up the field names via `model.get_result_field_names(layer.id())`, keyed
  by the actual owning layer id — the grid-owned layer id in modes 1/2, or
  the result-owned layer id in mode 3.
- On reopen, `load_grid()`/`load_result()` regenerate the dynamic fields
  from scratch (with fresh UUIDs), exactly like a first-time load.

### Deferred layers on restore

The same deferral decision described above is made again when a QGIS
project is reopened. `ThreeDiPluginModelSerializer` reads each `<grid>` XML
node's `<result>` children before calling `load_grid()`: if the grid has at
least one result child and *all* of them carry a non-empty `layer_path`,
the restored `ThreeDiGridItem` is marked `defer_layer_creation = True` as
well, so a saved-and-reopened purely-isolated project does not recreate the
orphaned unisolated layer tree on every reopen. If any child result has no
`layer_path` (mixed use, or plain standalone/project-based use), the grid
restores and loads its own layers immediately, exactly like a fresh
(non-restored) load would.

```mermaid
flowchart TD
    A["_read_recursive() reaches a &lt;grid&gt; XML node"] --> B["scan its &lt;result&gt; children"]
    B --> C{"at least one result child,\nand all have layer_path?"}
    C -->|"yes"| D["model_node.defer_layer_creation = True"]
    C -->|"no"| E["defer_layer_creation stays False"]
    D --> F["loader.load_grid(model_node, project)"]
    E --> F
```

Isolated result nodes persist their own `layer_path` and result-owned
`<layer>` children directly on the `<result>` XML element (in addition to
the regular `<layer>` children a `<grid>` element carries for its own,
non-deferred layers), so isolated layers are reused rather than duplicated
on reopen.
