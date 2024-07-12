import sys
from pkg_resources import get_distribution, DistributionNotFound, RequirementParseError

def get_dependency_version(package_name, dependency_name):
    try:
        dist = get_distribution(package_name)
        requires = dist.requires()
        for req in requires:
            if req.name == dependency_name:
                return req.specs[0][1] if req.specs else None
    except (DistributionNotFound, RequirementParseError) as e:
        print(f"Error getting {dependency_name} version for {package_name}: {e}")
        sys.exit(1)
    return None

def check_dependency_conflicts():
    modelchecker_schema_version = get_dependency_version('threedi-modelchecker', 'threedi-schema')
    gridbuilder_schema_version = get_dependency_version('threedigrid-builder', 'threedi-schema')

    if not modelchecker_schema_version or not gridbuilder_schema_version:
        print("Could not determine the required versions of threedi-schema.")
        sys.exit(1)

    print(f"Model Checker Schema Version: {modelchecker_schema_version}")
    print(f"Grid Builder Schema Version: {gridbuilder_schema_version}")

    if modelchecker_schema_version != gridbuilder_schema_version:
        print(f"Version conflict detected: threedi-modelchecker requires threedi-schema=={modelchecker_schema_version}, but threedigrid-builder requires threedi-schema=={gridbuilder_schema_version}")
        sys.exit(1)

    print("No version conflicts detected.")
    sys.exit(0)

def main():
    check_dependency_conflicts()

if __name__ == "__main__":
    main()
