"""Our crew is replaceable, your package isn't!"""
import subprocess
from pathlib import Path
from shutil import move
from typing import List

# NB: These are manually dependency sorted!
# TODO: Tree shaking or DAG or equivalent
PACKAGES: List[str] = [
    "python-dbus-next",
    "python-gmqtt",
    "python-pyquaternion",
    "python-astoria",
    "python-j5",
    "python-sr-robot3",
    # "srobo-kit",
]

CURR_PATH = Path(".")
BUILD_PATH = Path("/tmp/build")

def build_package(name: str) -> None:
    """Build it."""
    package_dir = CURR_PATH.joinpath(name)
    assert package_dir.exists()
    assert package_dir.joinpath("PKGBUILD").exists()
    print(f"\tFound directory and PKGBUILD")

    subprocess.run(["makepkg", "-si", "--noconfirm"], cwd=package_dir)

    package_files = [x for x in package_dir.glob("*.pkg.tar.*")]
    assert len(package_files) != 0
    print(f"\t{len(package_files)} packages have been produced.")

    for pkg in package_files:
        move(pkg, BUILD_PATH / pkg.name)

if __name__ == "__main__":
    print("PLANET EXPRESS PACKAGE DELIVERY")
    print(__doc__)
    print("")

    for package in PACKAGES:
        print(f"Building {package}")
        build_package(package)
