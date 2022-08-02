from setuptools import setup

package_name = "amcl_auto_localization"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="root",
    maintainer_email="pawel.kowalski@husarion.com",
    description="TODO: Package description",
    license="Apache License 2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "auto_localization_client = amcl_auto_localization.no_motion_update_client:main",
        ],
    },
)
