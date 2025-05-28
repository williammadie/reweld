import os

class PathHandler:

    @staticmethod
    def package_root_path() -> str:
        """
        Returns the root path of the package.
        """
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def project_root_path() -> str:
        """
        Returns the root path of the project.
        """
        return os.path.dirname(PathHandler.package_root_path())
    
    @staticmethod
    def test_directory_path() -> str:
        """
        Returns the path to the test directory.
        """
        return os.path.join(PathHandler.project_root_path(), "tests")
