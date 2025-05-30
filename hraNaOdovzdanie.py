import pygame
import random
import math

# code origin: https://github.com/Viliami/agario.git - not copied, rewrited and understood
#https://github.com/Viliami/agario/blob/master/agar.py
windowWidth, windowHeight = 1200, 750
platformWidth, platformHeight = 2000, 2000

pygame.init()
pygame.display.set_caption("{} ".format("JozefPupava Agar.io"))
clock = pygame.time.Clock()

font = pygame.font.Font("Ubuntu/Ubuntu-Regular.ttf",20)
 
mainSurface = pygame.display.set_mode((windowWidth, windowHeight))
scoreSurface = pygame.Surface((95, 25), pygame.SRCALPHA)
scoreSurface.fill((50,50,50,80))

def drawText(message,position, color=(255, 255, 255)):
    mainSurface.blit(font.render(message,1,color), position)

def getDistance(a,b):
    diffX = math.fabs(a[0]-b[0])
    diffY = math.fabs(a[1]-b[1])
    return ((diffX**2)+(diffY**2))**(0.5)



class Painter:
    def __init__(self):
        self.paintings = []

    def add(self, drawable):
        self.paintings.append(drawable)


    
        self.paintings.remove(drawable)

    def paint(self):
        for drawing in self.paintings:
            drawing.draw()



class Camera:
    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = windowWidth, windowHeight
        self.zoom = 0.5

    def centre(self, blobOrPosition):
        if isinstance(blobOrPosition, Player):
            x, y = blobOrPosition.x, blobOrPosition.y
            self.x = (x-(x*self.zoom)) - x + (windowWidth/2)
            self.y = (y-(y*self.zoom)) -y + (windowHeight/2)
        elif type(blobOrPosition) == tuple:
            self.x, self.y = blopOrPosition

    def update(self, target):
        self.zoom = 100/(target.mass)+0.3
        self.centre(blob)


        
class Drawable:

    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

class Grid(Drawable):
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = (230, 240, 240)

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0, 2001, 25):
            pygame.draw.line(self.surface, self.color, (x, i*zoom+y), (2001*zoom + x, i*zoom+y), 3)
            pygame.draw.line(self.surface, self.color, (i*zoom + x, y), (i*zoom +x, 2001*zoom + y), 3)



class HUD(Drawable):
    def __init__(self, surface, camera):
        super().__init__(surface, camera)

    def draw(self):
        w, h = font.size("Score: " + str(int(blob.mass*2))+" ")
        mainSurface.blit(pygame.transform.scale(scoreSurface, (w, h)), (8, windowHeight-30))
        drawText("Score: " + str(int(blob.mass*2)),(10,windowHeight-30))



class Player(Drawable):
    COLOR_LIST = [
    (37,7,255),
    (35,183,253),
    (48,254,241),
    (19,79,251),
    (255,7,230),
    (255,7,23),
    (6,254,13)]

    FONT_COLOR = (50, 50, 50)
    
    def __init__(self, surface, camera, name = ""):
        super().__init__(surface, camera)
        self.x = random.randint(100,700)
        self.y = random.randint(100,700)
        self.mass = 200
        self.speed = 3
        self.color = col = random.choice(Player.COLOR_LIST)
        self.outlineColor = (
            int(col[0]-col[0]/3),
            int(col[1]-col[1]/3),
            int(col[2]-col[2]/3))
        if name: self.name = name
        else: self.name = "Anonymous"
        self.pieces = []


    def collisionDetection(self, edibles):
        for edible in edibles:

            if(getDistance((edible.x, edible.y), (self.x,self.y)) <= self.mass/2):
                self.mass+=0.5
                edibles.remove(edible)


    def move(self):
       
        dX, dY = pygame.mouse.get_pos()
        rotation = math.atan2(dY - float(windowHeight)/2, dX - float(windowWidth)/2)
        rotation *= 180/math.pi
        normalized = (90 - math.fabs(rotation))/90
        vx = self.speed*normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        self.x = tmpX
        self.y = tmpY

    def feed(self):
        """Unsupported feature.
        """
        pass

    def split(self):
        """Unsupported feature.
        """
        pass

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        
        pygame.draw.circle(self.surface, self.outlineColor, center, int((self.mass/2 + 3)*zoom))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass/2*zoom))
        fw, fh = font.size(self.name)
        drawText(self.name, (self.x*zoom + x - int(fw/2), self.y*zoom + y - int(fh/2)),
                 Player.FONT_COLOR)


#I made entities on map


class Entity(Drawable):
    COLOR_LIST = [
    (37,7,255),
    (35,183,253),
    (48,254,241),
    (19,79,251),
    (255,7,230),
    (255,7,23),
    (6,254,13)]

    FONT_COLOR = (50, 50, 50)
    
    def __init__(self, surface, camera, name = ""):
        super().__init__(surface, camera)
        self.x = random.randint(400,1500)
        self.y = random.randint(400,1500)
        self.mass = 20
        self.speed = 3
        self.color = col = random.choice(Entity.COLOR_LIST)
        self.outlineColor = (
            int(col[0]-col[0]/3),
            int(col[1]-col[1]/3),
            int(col[2]-col[2]/3))
        if name: self.name = name
        else: self.name = "Anonymous"
        self.pieces = []


    def collisionDetection(self, edibles):
        for edible in edibles:
            if(getDistance((edible.x, edible.y), (self.x,self.y)) <= self.mass/2):
                self.mass+=1
                edibles.remove(edible)


    def move(self, dX, dY):
       
        #dX, dY = pygame.mouse.get_pos()

        #print(self.x, self.y)

        if self.x < 0:
            dX = random.randint(500, platformWidth - 20)
        elif self.x > platformWidth:
            dX = random.randint(0, 500)
        if self.y < 0:
            dY = random.randint(500, platformHeight -20)
        elif self.y > platformHeight:
            dY = random.randint(0, 500)
            
        rotation = math.atan2(dY - float(windowHeight)/2, dX - float(windowWidth)/2)
        rotation *= 180/math.pi
        normalized = (90 - math.fabs(rotation))/90
        vx = self.speed*normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        self.x = tmpX
        self.y = tmpY

    def feed(self):
        """Unsupported feature.
        """
        pass

    def split(self):
        """Unsupported feature.
        """
        pass

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        
        pygame.draw.circle(self.surface, self.outlineColor, center, int((self.mass/2 + 3)*zoom))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass/2*zoom))
        fw, fh = font.size(self.name)
        drawText(self.name, (self.x*zoom + x - int(fw/2), self.y*zoom + y - int(fh/2)),
                 Entity.FONT_COLOR)







        


class Cell(Drawable): 
    CELL_COLORS = [
    (80,252,54),
    (36,244,255),
    (243,31,46),
    (4,39,243),
    (254,6,178),
    (255,211,7),
    (216,6,254),
    (145,255,7),
    (7,255,182),
    (255,6,86),
    (147,7,255)]
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 7
        self.color = random.choice(Cell.CELL_COLORS)

    def draw(self):
        zoom = self.camera.zoom
        x,y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass*zoom))
       


class CellList(Drawable):

    def __init__(self, surface, camera, numOfCells):
        super().__init__(surface, camera)
        self.count = numOfCells
        self.list = []
        for i in range(self.count):
            self.list.append(Cell(self.surface, self.camera))

    def draw(self):
        for cell in self.list:
            cell.draw()



entityList = []            


cam = Camera()
grid = Grid(mainSurface, cam)

blob = Player(mainSurface, cam, "Peter")
hud = HUD(mainSurface, cam)
ent = Entity(mainSurface, cam, "jano")
entityList.append(ent)

cells = CellList(mainSurface, cam, 2000)

painter = Painter()
painter.add(grid)
painter.add(cells)
painter.add(blob)
painter.add(hud)
painter.add(ent)

helpVar = 70
dX = random.randint(0, 1980)
dY = random.randint(0, 1980)
while(True):
    
    clock.tick(70)
    
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if(e.key == pygame.K_SPACE):
                del(cam)
                blob.split()
            if(e.key == pygame.K_w):
                blob.feed()
        if(e.type == pygame.QUIT):
            pygame.quit()
            quit()

    

    if entityList:
        ent.move(dX, dY)
        ent.collisionDetection(cells.list)
        if helpVar > 0:
             helpVar = helpVar-1
        else:
            dX = random.randint(50, 1000)
            dY = random.randint(50, 1000)
            print(dX, dY)
            helpVar= 70
    else:
        painter = None
        painter = Painter()
        painter.add(grid)
        painter.add(cells)
        painter.add(blob)
        painter.add(hud)
    
        
        
    blob.move()
    blob.collisionDetection(cells.list)
    blob.collisionDetection(entityList)
    cam.update(blob)
    cam.update(ent)
    mainSurface.fill((242, 251, 255))
    painter.paint()
    pygame.display.flip()

    




                                
                    

            
