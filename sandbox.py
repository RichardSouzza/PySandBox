import pygame
from assets.colors import colors
from blocks import Air, Water
from random import choice


class SandBox:
    def __init__(self, root, x, y, size_hint_x, size_hint_y):
        self.root = root
        self.width = root.width * size_hint_x
        self.height = round(root.height * size_hint_y)
        self.screen = root.screen.subsurface(x, y, self.width, self.height)
        self.bg_color = colors["black"]
        self.blocks_list = []
        self.gravt = 8
        self.build()
    
    def build(self):
        if self.width < self.height:
            self.cols_number = 32
            self.cols_width = round(self.width / self.cols_number)
            self.make_columns()
            self.rows_height = self.cols_width
            self.rows_number = round(self.height / self.rows_height)
            self.make_rows()
        
        else:
            self.rows_number = 32
            self.rows_height = round(self.height / self.rows_number)
            self.make_rows()
            self.cols_width = self.rows_height
            self.cols_number = round(self.width / self.cols_width)
            self.make_columns()
    
    def blocks_per_column(self, col, blocks_list=None):
        if blocks_list == None:
            blocks_list = self.blocks_list 
        
        blocks = []
        for block in blocks_list:
            if block.col == col:
                blocks.append(block)
        
        return blocks
    
    def blocks_per_row(self, row, blocks_list=None):
        if blocks_list == None:
            blocks_list = self.blocks_list 
        
        blocks = []
        for block in blocks_list:
            if block.row == row:
                blocks.append(block)
        
        return blocks
    
    def draw(self):
        self.screen.fill(self.bg_color)
        for block in self.blocks_list:
            if type(block) == Air:
                self.remove_block(block)
            else:
                block.draw(self.screen)
    
    def fill(self):
        for block in self.blocks_list:
            if type(block) == Water:
                col = block.col
                row = self.blocks_per_row(block.row)
                bottom = self.blocks_per_row(block.row + 1)
                left_col = col
                right_col = col
                block_in_left = False
                block_in_right = False
                direction = None
                
                if block.collision_y(bottom):
                    for count in range(len(bottom)):
                        if left_col > 0:
                            left_col = col - count - 1
                        if right_col < self.cols_number - 1:
                            right_col = col + count + 1
                        
                        left = self.blocks_per_column(left_col, row)
                        right = self.blocks_per_column(right_col, row)
                        b_left = self.blocks_per_column(left_col, bottom)
                        b_right = self.blocks_per_column(right_col, bottom)
                        
                        if any(left) and Water not in left:
                            block_in_left = True
                        if any(right) and Water not in right:
                            block_in_right = True
                        
                        if not any(b_left) and not any(b_right):
                            if block.col == 0:
                                direction = "right"
                            elif block.col == self.cols_number-1:
                                direction = "left"
                            else:
                                direction = choice(("left", "right"))
                            break
                        
                        elif not any(b_left) and block.col > 0:
                            direction = "left"
                            break
                        
                        elif not any(b_right) and block.col < self.cols_number-1:
                            direction = "right"
                            break
                
                if direction == "left" and not block_in_left:
                    block.rect.x -= self.cols_width
                
                elif direction == "right" and not block_in_right:
                    block.rect.x += self.cols_width
                
                block.col = self.get_col(block.rect.centerx)
    
    def get_col(self, x):
        cols = self.cols + [x]
        cols.sort()
        col = cols.index(x)-1
        return col
    
    def get_row(self, y):
        rows = self.rows + [y]
        rows.sort()
        row = rows.index(y)-1
        return row
    
    def gravity(self):
        for block in self.blocks_list:
            if block.fall and block.rect.bottom < self.height:
                blocks = []
                for blk in self.blocks_per_column(block.col):
                    if blk.rect.y > block.rect.y:
                        blocks.append(blk)
                
                if self.height - block.rect.bottom >= self.gravt:
                    block.move_y(self.gravt, blocks)
                else:
                    block.move_y(self.height - block.rect.bottom, blocks)
                
                block.row = self.get_row(block.rect.centery)
    
    def make_block(self, block, x, y):
        # Get column:
        col = self.get_col(x)
        x = self.cols[col]
        # Get row:
        row = self.get_row(y)
        y = self.rows[row]
        # Make block:
        block = block()
        block.set_rect(col, row, x, y, self.cols_width)
        self.blocks_list.append(block)
    
    def make_columns(self):
        self.cols = []
        for col in range(self.cols_number):
            self.cols.append(col * self.cols_width)
            pygame.draw.rect(
                self.screen,
                self.bg_color,
                (self.cols[col], 0,
                self.cols_width, self.height)
            )
    
    def make_rows(self):
        self.rows = []
        for row in range(self.rows_number):
            self.rows.append(row * self.rows_height)
            pygame.draw.rect(
                self.screen,
                self.bg_color,
                (0, self.rows[row],
                self.width, self.rows_height-1)
            )
    
    def remove_block(self, air_block):
        for block in self.blocks_list:
            if block.rect.collidepoint(air_block.rect.center):
                self.blocks_list.remove(block)
    
    def slide(self):
        for block in self.blocks_list:
            if block.fall and block.rect.bottom < self.height:
                bottom = self.blocks_per_row(block.row + 1)
                b_left = self.blocks_per_column(block.col - 1, bottom)
                b_right = self.blocks_per_column(block.col + 1, bottom)
                direction = None
                
                if block.collision_y(bottom):
                    if not any(b_left) and not any(b_right):
                        if block.col == 0:
                            direction = "right"
                        elif block.col == self.cols_number-1:
                            direction = "left"
                        else:
                            direction = choice(("left", "right"))
                    
                    elif not any(b_left) and block.col > 0:
                        direction = "left"
                    
                    elif not any(b_right) and block.col < self.cols_number-1:
                        direction = "right"
                
                if direction == "left":
                    block.rect.x -= self.cols_width
                    block.rect.y += self.rows_height - self.gravt
                
                elif direction == "right":
                    block.rect.x += self.cols_width
                    block.rect.y += self.rows_height - self.gravt
                
                block.col = self.get_col(block.rect.centerx)
                block.row = self.get_row(block.rect.centery)
