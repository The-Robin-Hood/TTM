    
class SemVer:
    def __init__(self, version) -> None:
        self.version = version
        
    def __repr__(self) -> str:
        return f"{self.version}"

    def __eq__(self, other):
        if isinstance(other, SemVer):
            return self.version == other.version

    def __ne__(self, other):
        if isinstance(other, SemVer):
            return self.version != other.version

    def __lt__(self, other):
        if isinstance(other, SemVer):
            return self.compare_versions(self.version, other.version) < 0

    def __gt__(self, other):
        if isinstance(other, SemVer):
            return self.compare_versions(self.version, other.version) > 0

    def __le__(self, other):
        if isinstance(other, SemVer):
            return self.compare_versions(self.version, other.version) <= 0

    def __ge__(self, other):
        if isinstance(other, SemVer):
            return self.compare_versions(self.version, other.version) >= 0

    @staticmethod
    def compare_versions(version1, version2):
        parts1 = version1.split('.')
        parts2 = version2.split('.')

        for i in range(max(len(parts1), len(parts2))):
            part1 = int(parts1[i]) if i < len(parts1) else 0
            part2 = int(parts2[i]) if i < len(parts2) else 0

            if part1 < part2:
                return -1
            elif part1 > part2:
                return 1
        return 0