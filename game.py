class Game:
    def __init__(self):
        self.grid = [[0 for x in range(10)] for y in range(10)]
        self.placeBegin()


    def placeBegin(self):
        for i,j in enumerate(self.grid):
            for k,l in enumerate(j):
                if i%2==0:
                    if k%2==0:
                        self.grid[i][k]=1
                else:
                    if k%2==1:
                        self.grid[i][k]=1
        print(self.grid)




test = Game()
test.placeBegin()
