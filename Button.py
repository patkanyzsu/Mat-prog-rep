import pygame

class Button():
    def __init__(self, x, y, image1, image2, scale): #initialization 
        width=image1.get_width() #get the parameters of the image
        height=image1.get_height()
        self.image1 = pygame.transform.scale(image1, (int(width*scale), int(height*scale))) #scaling of the img
        self.image2 = pygame.transform.scale(image2, (int(width*scale), int(height*scale))) #second phase of the circle
        self.rect = self.image1.get_rect() #hitbox
        self.rect.topleft = (x,y) #position
        self.clicked = False 
        self.shown = True #can the user see it?
        self.set = 0
    def draw(self, surface):
        if self.clicked:
            surface.blit(self.image2, (self.rect.x, self.rect.y)) #drawing the buttons
        else:
            surface.blit(self.image1, (self.rect.x, self.rect.y)) #drawing the other form
    def clicking(self, pos):
        action = False
        if self.rect.collidepoint(pos) and self.shown == True: #if the cursor is inside the image's invisible rectangle and can be clicked
            if pygame.mouse.get_pressed()[0] == 1: #if you LEFT click while the cursor is inside
                self.clicked = not self.clicked #change according to value (negate)
        if pygame.mouse.get_pressed()[2] == 1: #if you RIGHT click
                self.clicked = False
        # if pygame.mouse.get_pressed()[1] == 1: #if you MIDDLE click (for developement purposes)
        #         self.clicked = True
        action = self.clicked
        return action