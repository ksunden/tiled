from os import path
import setuptools

here = path.abspath(path.dirname(__file__))


def read_requirements(filename):
    with open(path.join(here, filename)) as requirements_file:
        # Parse requirements.txt, ignoring any commented-out lines.
        requirements = [
            line
            for line in requirements_file.read().splitlines()
            if not line.startswith("#")
        ]
    return requirements


extras_require = {
    key: read_requirements(f"requirements-{key}.txt")
    for key in ["client", "server", "array", "dataframe"]
}
extras_require["complete"] = sorted(set(sum(extras_require.values(), [])))

setuptools.setup(
    name="catalog_server",
    install_requires=[],  # Requirements depend strongly on use case (e.g. client vs server).
    extras_require=extras_require,
    packages=setuptools.find_packages(where=".", exclude=["doc", ".ci"]),
    entry_points={
        "catalog_server.special_client": [
            # This can be distributed in a separate, bluesky-focused
            # library someday.
            "BlueskyRun = catalog_server.client.bluesky:BlueskyRun",
        ],
        "catalog_server.container": [
            "array = catalog_server.client.array:ClientArraySource",
            "variable = catalog_server.client.xarray:ClientVariableSource",
            "data_array = catalog_server.client.xarray:ClientDataArraySource",
        ],
    },
)
