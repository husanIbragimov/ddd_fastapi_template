import importlib
import pkgutil


def import_all_from_package(package_name: str) -> None:
    package = importlib.import_module(package_name)  # Paketni import qilish
    package_path = package.__path__

    for _, module_name, is_pkg in pkgutil.walk_packages(package_path, package.__name__ + "."):
        importlib.import_module(module_name)  # Modulni import qilish

        # Agar modul bo'lsa, `from module import *` bajarish
        if not is_pkg:
            exec(f"from {module_name} import *", globals())

        # Agar package bo'lsa, rekursiv chaqirish
        if is_pkg:
            import_all_from_package(module_name)
