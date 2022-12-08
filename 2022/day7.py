from util import read_input

lines = read_input("inputs/day7.txt")


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self):
        return f"File({self.name}, {self.size})"


class Dir:
    def __init__(self, name, parent = None):
        self.name = name
        self._contents = {}
        self.parent = parent

    def add_file(self, file):
        self._contents[file.name] = file

    def add_dir(self, dir):
        self._contents[dir.name] = dir

    def cd(self, dirname):
        return self._contents[dirname]

    @property
    def size(self):
        return sum([file.size for file in self._contents.values()])

    def contents(self):
        return self._contents.values()

    def get_dirs(self):
        res = []
        for dirFile in self.contents():
            if isinstance(dirFile, Dir):
                res.append(dirFile)
                res += dirFile.get_dirs()
        return res


    def __str__(self):
        return f"Dir(name: {self.name}, parent: {self.parent.name if self.parent else None}, contents: {[str(e) for e in self._contents.values()]})"


inls = False
root = Dir("/")
curr = root
for l in lines:
    # print(curr.name, ",", l)
    if l.startswith("$"):
        args = l.split(" ")
        command = args[1]
        if command == "cd":
            cdTo = args[2]
            if cdTo == "..":
                curr = curr.parent
            elif cdTo == "/":
                curr = root
            else:
                curr = curr.cd(cdTo)
        elif command == "ls":
            inls = True
        else:
            print("command is not cd or ls\n")
    elif inls:
        sizeOrDir, name = l.split(" ")
        if sizeOrDir == "dir":
            curr.add_dir(Dir(name, curr))
        else:
            curr.add_file(File(name, int(sizeOrDir)))

# print(root)

# part 1
curr = root
st = [curr]
res = 0
while st:
    curr = st.pop()
    # print("pop", curr)
    if isinstance(curr, Dir):
        size = curr.size
        if size <= 100000:
            # print("dir is less than 100000", curr.size, curr)
            res += size
        for dirFile in curr.contents():
            # print("add", dirFile)
            st.append(dirFile)

print(res)


# part 2
all_dirs = [root] + root.get_dirs()
all_dirs_sizes = sorted([dir.size for dir in all_dirs])
curr_free = 70000000 - root.size
space_to_free = 30000000 - curr_free
for dir_size in all_dirs_sizes:
    if dir_size >= space_to_free:
        break
print(dir_size)