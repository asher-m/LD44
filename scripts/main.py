#!/usr/bin/env python3
""" Universal Blood Supply

A game by Asher Merrill for Ludum Dare 44.
"""

import pygame
import sys

pygame.init()

__myname__ = "Universal Blood Supply"
__title__ = "Universal Blood Supply"
__author__ = "h4ck3r_d00d (aka asher_m on Github)"
__version__ = "0.0pre"

CAPTION = f"{__title__} {__version__}"


# Default window dimensions:
DEFAULTWIDTH = 1440
DEFAULTHEIGHT = 900

# Game framerate, DO NOT ADJUST
FPS = 60
CLOCK = pygame.time.Clock()

# Colors:
BLACK = (0, 0, 0)
GOLD = (255, 167, 0)
GRAY_LIGHT = (220, 220, 220)
GRAY_UP = (155, 155, 155)
GRAY_DOWN = (50, 50, 50)
GREEN_UP = (103, 212, 37)
GREEN_DOWN = (29, 168, 37)
RED = (255, 0, 0)
RED_UP = (219, 0, 0)
RED_DOWN = (100, 0, 0)
WHITE = (255, 255, 255)


# Fonts:
FONT = pygame.font.Font("resources/cour.ttf", 14)
BOLDFONT = pygame.font.Font("resources/courbd.ttf", 14)

class Game:
    def __init__(self, again=False):
        """ Method to initialize Game class. """
        # System play variables:
        # Define the size of the screen:
        self.size = (DEFAULTWIDTH, DEFAULTHEIGHT)

        # Init display/window:
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption(CAPTION)
        icon = pygame.image.load("resources/icon_large.png")
        pygame.display.set_icon(icon)
        self.display.fill(WHITE)

        # Update/set the position of the mouse:
        self.mouse = pygame.mouse.get_pos()

        # Create vars dict that can be passed down:
        self.vars = {}

        # Welcome message:
        self.vars['log'] = ["Welcome to Universal Blood Supply!",
                    "Admittedly, you're a bit down on your luck, but you just "
                    "learned you can sell blood blood...",
                    "Maybe this will be how "
                    "you can finally pay off college..."]

        # Game mechanic variables:
        # Need an alive stat:
        self.alive = True

        # Define speed of game:
        self.vars['speed'] = 1.
        # Cost of living, (can be changed.) BY DEFAULT 1 MONEY PER SECOND:
        self.vars['upkeep'] = 3. / 720.
        # Starting money while here, used to keep currency later:
        self.vars['money'] = 12.
        # Blood:
        self.vars['blood'] = 100.
        # Max blood, maybe for something vampiric...
        self.max_blood = 100.
        # Regen rate:
        self.regen = 1./48.
        # Lastly the total sold:
        self.vars['blood_sold'] = 0
        # Blood to unit conversion ratio (ie., divide blood sold by this...):
        self.vars['blood_unit_conversion'] = 60
        # Get this percent going:
        self.vars['character_blood_percent'] = self.vars['blood'] / \
            self.max_blood * 100
        # That should be all the initialization required...


        # Sell blood manual stuff:
        # How much blood blood is sold each time:
        self.sell_blood_manual_sold = 60.
        # How much blood is sold for:
        self.sell_blood_manual_price = 24.

        # List of all researches and whether or not to allow them now:
        self.tech_0 = False # etc...


    def exit(self):
        """ Method to safely close. """
        print("Exiting...")
        pygame.quit()
        sys.exit()

    def main(self):
        """ Main method. """
        i = 0
        while True:
            self.event()
            self.update()
            self.draw()
            self.update_display()
            i += 1
            if i % 300 == 0:
                self.vars['log'].append(f"New line...i = {i}")

    def update(self):
        """ Method to update current balances of things,
        (and other numbers as they become relevant.) """
        # Check to make sure we're alive:
        if self.vars['money'] <= 0 or self.vars['blood'] <= 0:
            if self.vars['money'] < 0:
                self.vars['money'] = 0
            if self.vars['blood'] < 0:
                self.vars['blood'] = 0
            # Set state to dead if we are...
            self.alive = False
            if not elements['console_dead_notice'].active:
                elements['console_dead_notice'].active = True

        # Do these if we're alive:
        if self.alive:
            # Subtract cost from money:
            self.vars['money'] -= self.vars['upkeep'] * self.vars['speed']
            # Add however much we've regened:
            if self.vars['blood'] < 100.:
                self.vars['blood'] += self.regen * self.vars['speed']
                # Truncate if we've gone over:
                if self.vars['blood'] > self.max_blood:
                    self.vars['blood'] = self.max_blood

            # Regulars:
            # Can put regularly updated elements here, or below, depending...
            self.research_allow()

        # Get this percent going:
        self.vars['character_blood_percent'] = self.vars['blood'] / \
            self.max_blood * 100

    def event(self):
        """ Method to evaluate events since last tick. """
        # Update the position of the mouse:
        self.mouse = pygame.mouse.get_pos()
        # Process event queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and \
            event.key in (pygame.K_ESCAPE, pygame.K_q):
                self.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                # Set gameFunction to None:
                gameFunction = None
                # Process generic entities:
                for elem_name, elem_obj in elements.items():
                    if elem_obj.mouse_over(self.mouse):
                        # Lookup the game function, according to the type:
                        if isinstance(elem_obj, (Button, Text)):
                            gameFunction = elem_obj.gameFunctionName()
                        elif isinstance(elem_obj, Container):
                            gameFunction = \
                                elem_obj.gameFunctionName(self.mouse)
                if not gameFunction:
                    # Process entities in the research queue:
                    gameFunction = self.event_research_queue()
                # Now call the game function:
                if gameFunction:
                    print(gameFunction)
                    gameFunction(self)
                else:
                    print("Null event processed.  (Some user interaction not on a button...)")

    def event_null(self):
        """ A null event for the death notification, and possibly others... """
        pass

    def event_research_queue(self):
        """ Method to check if any research interactions occurred.

        Returns gameFunction from whatever button was depressed. """
        # Select what researches are unlocked and next in the queue:
        for j, v in enumerate([i for i in research if i['class'].unlocked
                               == True and i['class'].active == False][:3]):
            # Spoof mouse location so we can get buttons right:
            mouse = (self.mouse[0] - 1140, self.mouse[1] - 100 - (18 + 194 * j))
            # Ask if any of the buttons are active:
            for b in v['actions']:
                if b.mouse_over(mouse):
                    # Lookup the game function, according to the type:
                    if isinstance(b, (Button, Text)):
                        gameFunction = b.gameFunctionName()
                    elif isinstance(b, Container):
                        gameFunction = b.gameFunctionName(mouse)
                    return gameFunction

    def event_console_speed_up(self):
        """ Console speed control functions. """
        if self.alive:
            if self.vars['speed'] < 9999.9999:
                self.vars['speed'] *= 1.2
                if self.vars['speed'] > 9999.9999:
                    self.vars['speed'] = 9999.9999

    def event_console_speed_normal(self):
        """ Console speed control functions. """
        if self.alive:
            self.vars['speed'] = 1.

    def event_console_speed_down(self):
        """ Console speed control functions. """
        if self.alive:
            if self.vars['speed'] > 0.0001:
                self.vars['speed'] *= 1. / 1.2
                if self.vars['speed'] < 0.0001:
                    self.vars['speed'] = 0.0001

    def event_sell_blood_manual(self):
        """ Method to manually sell blood. """
        if self.alive:
            self.vars['blood'] -= self.sell_blood_manual_sold
            self.vars['money'] += self.sell_blood_manual_price
            self.vars['blood_sold'] += self.sell_blood_manual_sold


    def draw(self):
        """ Method to draw the screen each time a frame is requested. """
        # Handle some "constants", (ie., elements that always exist:)
        self.draw_console()
        self.draw_research_queue()
        self.draw_character()

        # Now draw the buttons:
        for elem_name, elem_obj in elements.items():
            # We need to only draw active objects and things that aren't
            # researches.  The research queue thing will handle researches.
            if elem_obj.active and not elem_name.startswith('research'):
                if isinstance(elem_obj, Button):
                    elem_obj.draw(self.display, self.mouse)
                elif isinstance(elem_obj, Text):
                    elem_obj.draw(self.display, self.vars)
                else:  # It's a container:
                    elem_obj.draw(self.display, self.mouse, self.vars)

    def draw_console(self):
        """ Method to draw the console section of the screen (top 100px), and
        elements containted within. """
        # Create a console surface:
        console = pygame.Surface((1440, 100))
        console.fill(GRAY_LIGHT)
        console_waterfall = pygame.Surface((780, 80))
        console_waterfall.fill(WHITE)
        # Blit all text in the text queue to the waterfall:
        for i, t in enumerate(self.vars['log'][-5:]):
            msg = FONT.render(t, True, BLACK)
            msg_loc = msg.get_rect()
            msg_loc.centery = 8 + i * 16
            msg_loc.x = 4
            console_waterfall.blit(msg, msg_loc)
        console.blit(console_waterfall, (220, 10))
        disp_text_center(console, FONT,
                         f"Game Speed: {self.vars['speed']:9.4f}", BLACK,
                         (220 / 2, (100 - 62) / 2 + 62))

        # Now blit the current status of bank accounts and health:
        # Draw labels for the other elements:
        disp_text_center_vertical(console, BOLDFONT, "HEALTH", RED, (1020, 34))
        disp_text_center_vertical(console, BOLDFONT, "MONEY", GOLD, (1020, 50))
        disp_text_center_vertical(console, BOLDFONT,
                                  "UNITS SOLD", BLACK, (1020, 66))
        disp_text_center_vertical(console, FONT, "{:<40s}".format(
            str("*" * int(40 * self.vars['blood'] / self.max_blood))), RED, (1105, 34))
        disp_text_center_vertical(console, FONT, "$" + f"{self.vars['money']:39.2f}", BLACK, (1105, 50))
        # Round off out units sold so it looks nice:
        units_sold = round(self.vars['blood_sold'] / self.vars['blood_unit_conversion'])
        disp_text_center_vertical(console, FONT, f"{units_sold:40d}", BLACK, (1105, 66))

        # Finally blit display:
        self.display.blit(console, (0, 0))

    def draw_character(self):
        """ Method to draw and animate the character correctly. """
        character = pygame.Surface((300, 200))
        character.fill(GRAY_LIGHT)
        text = Text("The character will\n"
                    "go here with animations\n"
                    "correspondingto blood\n"
                    "percent: {character_blood_percent:5.2f}%.\n"
                    "12345678901234567890123456789012345678901234567890", RED, (0, 0),
                    font=FONT, centerx=False, centery=False)

        text.draw(character, self.vars)
        self.display.blit(character, (1140, 700))

    def draw_research_queue(self):
        """ Method to draw what researches are available. """
        # Start by defining the surface that we're working in:
        queue = pygame.Surface((300, 600))
        queue.fill(GRAY_LIGHT)
        # Draw dialogue title:
        title = Text("Available Research".upper(), BLACK, (5, 18/2),
                     font=BOLDFONT, centerx=False, centery=True)
        title.draw(queue)

        # Select what researches are unlocked and next in the queue:
        for j, v in enumerate([i for i in research if i['class'].unlocked
                               == True and i['class'].active == False][:3]):
            # Spoof mouse location so we can get buttons right:
            mouse = (self.mouse[0] - 1140, self.mouse[1] - 100 - (18 + 194 * j))
            # Create the techWindow from the tech's class:
            techWindow = v['class'].draw(mouse, self.vars)
            # Draw the buttons:
            for b in v['actions']:
                b.draw(techWindow, mouse)
            # Draw the tech window into the queue window:
            queue.blit(techWindow, (0, 18 + 194 * j))
        # Draw the queue window:
        self.display.blit(queue, (1140, 100))


    def draw_dead(self):
        """ Method to display scores and pause game. """

    def update_display(self):
        """ Method to update the display. """
        pygame.display.update()
        CLOCK.tick(FPS)

    def research_allow(self):
        """ Method that checks if new techs in each tree should be
        unlocked, AND if any mutually exclusive techs are used.

        (The latter bit is also accomplished in various Research.activate()
        methods.) """
        sci = [i for i in research if i['tree'] == treeScientific]
        soc = [i for i in research if i['tree'] == treeSocial]
        spi = [i for i in research if i['tree'] == treeSpiritual]

        # For each tree, check if the previous tech has been researched:
        # Find next locked tech:
        for l in [sci, soc, spi]:
            # Get statuses of all techs:
            unlocked = [i['class'].unlocked for i in l]
            # Get index of first locked tech, (ie., all previous techs locked)
            if not all(unlocked):
                # Make sure we still have locked techs:
                j = unlocked.index(False)
            else:
                # If not, continue:
                continue
            # If we're allowed to unlock it, do so:
            if l[j]['class'].allow_unlock(self.vars):
                l[j]['class'].unlocked = True

    def research_activate_Hematology(self):
        """ Method to activate the Hematology research.

        Modify internal parameters and then call the Hematology class's
        activate method to finish the job. """
        # Update class vars from what Hematology says:
        self.vars['money'] -= Hematology.cost
        self.vars['upkeep'] *= Hematology.upkeep_mult
        self.regen *= Hematology.regen_mult
        # Find the correct instance of Hematology:
        for v in research:
            if isinstance(v['class'], Hematology):
                v['class'].activate()


class Container:
    """ A class that has methods useful for determining if elements inside it
    are moused over, and can be used to abstract some of the position/alignment
    away from the top level. """
    def __init__(self, color, dims, subelems, active=False, human_name=None):
        self.color = color
        self.xloc = dims[0]
        self.yloc = dims[1]
        self.width = dims[2]
        self.height = dims[3]
        self.subelems = subelems
        self.active = active
        self.human_name = human_name

    def gameFunctionName(self, mouse):
        """ Method to return the name of the function to be executed by the
        game upstream. """
        # Adjust mouse values according to container's position:
        mouse = (mouse[0] - self.xloc, mouse[1] - self.yloc)
        # For each element that it could be:
        for i in self.subelems:
            # We can have buttons OR text here, possibly more in the future:
            if i.mouse_over(mouse) and isinstance(i, (Button,
                                                      Text)):
                return i.gameFunctionName()
            # If the object is a container, we need to hand it more info:
            elif i.mouse_over(mouse) and isinstance(i, Container):
                return i.gameFunctionName(mouse)

    def mouse_over(self, mouse):
        """ Method for determining if contained elements are moused over or
        not. """
        # Adjust mouse values according to container's position:
        mouse = (mouse[0] - self.xloc, mouse[1] - self.yloc)
        for i in self.subelems:
            # Need to handle the different types different again...
            if isinstance(i, (Button,  # Button and Container
                              Container
                              )) and i.mouse_over(mouse):
                return True
            elif isinstance(i, Text):  # Text
                i.mouse_over()
        return False

    def draw(self, display, mouse, fmtvars):
        """ Method to draw all elements within this container.
        fmtvars is a dict used to casting to format string. """
        # Adjust mouse values according to container's position:
        mouse = (mouse[0] - self.xloc, mouse[1] - self.yloc)
        # Now make the surface that is the container (us):
        container = pygame.Surface((self.width, self.height))
        container.fill(self.color)
        for i in self.subelems:
            # Need to handle the different types different again...
            if isinstance(i, Button):
                i.draw(container, mouse)
            elif isinstance(i, Text):
                i.draw(container, fmtvars)
            else:  # It's another container:
                i.draw(container, mouse, fmtvars)
        display.blit(container, (self.xloc, self.yloc))


class Text:
    """ A class for dumb text that  the user cannot interact with.

    Location is the coordinates of the textbox inside its parent surface,
    (defined when calling this method so text can be displayed multiple
    places.)  Location also depends on if centerx or centery is true. """
    def __init__(self, fmtstring, color, location,
                 active=False, human_name=None, font=None, centerx=True,
                 centery=True):
        """ Method to initialize Text object.

        fmtstring is a format string.  In Text.draw, this is used as:
            fmtstring.format(**fmtvars) """
        self.color = color
        self.fmtstring = fmtstring
        self.location = location
        self.xloc = location[0]
        self.yloc = location[1]
        self.active = active
        self.human_name = human_name
        self.centerx = centerx
        self.centery = centery
        if font:
            self.font = font
        else:
            self.font = FONT

    def gameFunctionName(self):
        """ A method to return the name of the function if this element
        is found to have been moused over and clicked. """
        return Game.event_null

    def mouse_over(self):
        """ Method to determine if the mouse is over top of this object. """
        return False

    def draw(self, display, fmtvars={}):
        """ Method to draw the text.

        fmtvar is a dictionary of vars according to their names in Game """
        # Make text string:
        text = self.fmtstring.format(**fmtvars)
        max_width = 0
        max_height = 0
        for phrase in text.splitlines():
            # Determine size of the rectangle to use:
            phrase_rend = self.font.render(phrase, True, self.color)
            phrase_box = phrase_rend.get_rect()
            if phrase_box.width > max_width:
                max_width = phrase_box.width
            if phrase_box.height > max_height:
                max_height = phrase_box.height

        # Now max a new surface with these dimensions:
        textbox = pygame.Surface((max_width, max_height * len(text.splitlines())), pygame.SRCALPHA)
        textbox.fill((0, 0, 0, 0))  # RGBA value, to make it transparent.  NOTE you have you use the pygame.SRCALPHA flag!

        # Now for each phrase, display the phrase on textbox aligned according
        # to parameters:
        for i, phrase in enumerate(text.splitlines()):
            # Determine the positon of phrase within textbox:
            if self.centerx:
                xloc = max_width / 2
            else:
                xloc = 0
            if self.centery:
                yloc = max_height / 2 + i * max_height
            else:
                yloc = i * max_height

            # Display that:
            if self.centerx and self.centery:
                # Text needs to be centered in dialog:
                disp_text_center(textbox, self.font, phrase, self.color,
                                 (xloc, yloc))
            elif self.centerx:
                # Text doesn't need to be centered in y:
                disp_text_center_horizontal(textbox, self.font, phrase,
                                          self.color, (xloc, yloc))
            elif self.centery:
                # Text needs to be centered in y and not in x:
                disp_text_center_vertical(textbox, self.font, phrase,
                                            self.color, (xloc, yloc))
            else:
                # Text doesn't need to be centered at all:
                disp_text(textbox, self.font, phrase,
                          self.color, (xloc, yloc))

        textbox_loc = textbox.get_rect()
        if self.centerx:
            textbox_loc.centerx = self.xloc
        else:
            textbox_loc.x = self.xloc
        if self.centery:
            textbox_loc.centery = self.yloc
        else:
            textbox_loc.y = self.yloc

        # Finally display all of that:
        display.blit(textbox, textbox_loc)

class Button:
    """ Class defining buttons and how they behave when things
    are over them. """
    def __init__(self, color_up, color_down, dims, gameFunction, active=False,
                 text=None, human_name=None, font=None):
        """ A class to hold the information about buttons.  Used to DRAW the
        screen AND to register using interaction, (ie., UPDATE.)

        For dims, tuple is: (upper left x, upper left y, width, height).
        First 2 elements of dims must be absolute position to have mouseover
        work correctly, UNLESS inside a container.

        ALL BUTTONS WITHIN CONTAINERS MUST BE ACTIVE TO APPEAR! """
        # Write these things:
        self.color_up = color_up
        self.color_down = color_down
        self.xloc = dims[0]
        self.yloc = dims[1]
        self.width = dims[2]
        self.height = dims[3]
        self.gameFuction = gameFunction
        self.active = active
        self.text = text
        self.human_name = human_name
        if font:
            self.font = font
        else:
            self.font = BOLDFONT

        # Define text location:
        self.text_location = tuple((self.width / 2, self.height / 2))

        # We can create the surfaces and any possible colors upfront so we
        # don't have to later:
        # UP (ie., mouse NOT over):
        self.up = pygame.Surface((self.width, self.height))
        self.up.fill(self.color_up)
        disp_text_center(self.up, self.font, text,
                         color_negative(self.color_up), self.text_location)
        # DOWN (ie., mouse over):
        self.down = pygame.Surface((self.width, self.height))
        self.down.fill(self.color_down)
        disp_text_center(self.down, self.font, text,
                         color_negative(self.color_down), self.text_location)

    def gameFunctionName(self):
        """ Method to return (upstream) the name of the function to be
        executed. """
        return self.gameFuction

    def mouse_over(self, mouse):
        """ Method to determine if a mouse is overtop of a button... """
        return (self.xloc < mouse[0] < self.xloc + self.width and
                self.yloc < mouse[1] < self.yloc + self.height)

    def draw(self, display, mouse):
        """ Method to draw the depressed (or undepressed) button. """
        if self.mouse_over(mouse):
            display.blit(self.down, (self.xloc, self.yloc))
        else:
            display.blit(self.up, (self.xloc, self.yloc))


class ResearchTree:
    """ A class defining if a research tree is allowable or not. """
    def __init__(self):
        self.allowed = True

    def lock(self):
        self.allowed = False


class Research:
    """ A class containing information about research.

    unlocked indicates a research is available and should be displayed in the
    research queue.
    active indicates that a research is complete. """
    def __init__(self, unlocked=False, active=False):
        self.unlocked = unlocked
        self.active = active

    def draw(self, mouse, fmtvars):
        """ Method to draw buttons and relevant text of tech. Returns a pygame
        surface that the caller will blit in the correct location. """
        techWindow = pygame.Surface((300, 194))
        techWindow.fill(GRAY_LIGHT)
        return techWindow

    def activate(self):
        """ Method to make changes to Game (enable/disable techs) if this is
        active, and set self active. """
        self.active = True
        # Generally, activate SHOULD unlock the next tech.

    def allow_unlock(self, fmtvars):
        """ Method to check if all conditions are valid to allow unlock. """


class Hematology(Research):
    """ A subclass of research.Opens Scientific branch:

        1. Increasing upkeep/cost (5%)
        2. Increase regen rate (30%) """
    """ Research Name """
    resName = "Hematology".upper()
    """ How much money to unlock this tech? """
    cost = 480.
    """ How much more upkeep does this cost? """
    upkeep_mult = 1.05
    """ How much more regen do we get? """
    regen_mult = 1.5

    # Create text string:
    text = "Purchase a hematology textbook for\n"\
           "${:6.2f} to learn how to eat better\n"\
           "and produce more blood. Increase\n"\
           "upkeep by {:4.2f}x AND increase regen\n"\
           "by {:4.2f}x.".format(cost, upkeep_mult, regen_mult)

    def draw(self, mouse, fmtvars):
        """ Method to draw buttons and stuff.

        Returns a pygame surface that the caller will blit in the correct
        location. """
        # Create a pygame surface:
        techWindow = super(Hematology, self).draw(mouse, fmtvars)
        # Draw a nice title:
        title = Text(Hematology.resName, GRAY_DOWN, (5, 5), font=FONT,
                     centerx=False, centery=False)
        title.draw(techWindow)

        # Now the explanation of the tech:
        words = Text(Hematology.text, BLACK, (10, 21), font=FONT,
                     centerx=False, centery=False)
        words.draw(techWindow)
        return techWindow

    def activate(self):
        print("IT WORKED MOTHERFUCKERS!")

    def allow_unlock(self, fmtvars):
        """ Method to check to make sure we have enough money over all time """
        if fmtvars['blood_sold'] / fmtvars['blood_unit_conversion'] > 20.:
            return True
        else:
            return False


def disp_text(surface, font, message, color, location):
    """ A function that prints a message in some
    color at the center of the screen. """
    msg_rend = font.render(message, True, color)
    msg_loc = msg_rend.get_rect()
    msg_loc.x = location[0]
    msg_loc.y = location[1]
    surface.blit(msg_rend, msg_loc)


def disp_text_center(surface, font, message, color, location):
    """ A function that prints a message in some
    color at the center of the screen. """
    msg_rend = font.render(message, True, color)
    msg_loc = msg_rend.get_rect()
    msg_loc.centerx = location[0]
    msg_loc.centery = location[1]
    surface.blit(msg_rend, msg_loc)


def disp_text_center_horizontal(surface, font, message, color, location):
    """ A function that prints a message in some
    color at the center of the screen in the x-direction, and
    wherever you tell it in y. """
    msg_rend = font.render(message, True, color)
    msg_loc = msg_rend.get_rect()
    msg_loc.centerx = location[0]
    msg_loc.y = location[1]
    surface.blit(msg_rend, msg_loc)


def disp_text_center_vertical(surface, font, message, color, location):
    """ A function that prints a message in some
    color at the center of the screen in the y-direction, and
    wherever you tell it in x. """
    msg_rend = font.render(message, True, color)
    msg_loc = msg_rend.get_rect()
    msg_loc.x = location[0]
    msg_loc.centery = location[1]
    surface.blit(msg_rend, msg_loc)


def color_negative(color):
    """ A function that takes in a 3 tuple of RGB values and then returns
    the rot-255 value of that color. """
    return tuple([int((i + 255/2) % 255) for i in color])


""" Dictionary of some elements in the game that are procedurally drawn... """
elements = {
        'console_dead_notice': Button(RED_UP, RED_UP, (220, 10, 780, 80), Game.event_null, active=False, text='!!! YOU ARE DEAD !!!'),
        'console_<<': Button(RED_UP, RED_DOWN, (25, 12, 50, 50), Game.event_console_speed_down, active=True, text='<<'),
        'console_==': Button(GRAY_UP, GRAY_DOWN, (85, 12, 50, 50), Game.event_console_speed_normal, active=True, text='=='),
        'console_>>': Button(GREEN_UP, GREEN_DOWN, (145, 12, 50, 50), Game.event_console_speed_up, active=True, text='>>'),
        'sell_blood_manual': Button(GRAY_UP, GRAY_DOWN, (10, 110, 96, 32), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
#        'test_container': Container(GRAY_LIGHT, (360, 250, 720, 400), [
#            Button(GRAY_UP, GRAY_DOWN, (10, 10, 100, 100), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
#            Button(GRAY_UP, GRAY_DOWN, (10, 210, 100, 100), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
#            Button(GRAY_UP, GRAY_DOWN, (210, 10, 100, 100), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
#            Button(GRAY_UP, GRAY_DOWN, (210, 210, 100, 100), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
#            Text("Text stuff... {blood}", RED, (410, 210, 100, 100), active=True, centerx=False, centery=False, human_name="test_container Blood Readout")
#            ], active=True),
        }

""" Available research trees: """
treeScientific = ResearchTree()
treeSocial = ResearchTree()
treeSpiritual = ResearchTree()


""" List of researches available in the game and their status. """
research = [
        {'tree':treeScientific, 'class':Hematology(unlocked=False), 'actions': [Button(GRAY_UP, GRAY_DOWN, (300 - 48 - 16, 194 - 32 - 16, 48, 32), Game.research_activate_Hematology, active=True, text="OK")]}
        ]


if __name__ == "__main__":
    g = Game()
    g.main()
