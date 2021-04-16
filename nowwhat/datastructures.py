
class Sources():
    def __init__(self, sourcespath=sourcespath):
        self.path = sourcespath

    def load_month(self, y, m):
        assert y in range(10, 22) and m in range(1, 13)
        y, m = str(y), str(m).zfill(2)
        if y<16 or (y==16 and m<11):
            print('Loading all sources for Jan 2010 through Oct 2016 ')
            self.src = pd.concat(
                        read_sources(join(self.path, f"now_sources_pt{i}.txt")
                        for i in [1, 2]), sort=False)
        else:
            self.src = read_sources(join(self.path, f"sources-{y}-{m}.txt")
