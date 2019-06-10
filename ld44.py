#!/usr/bin/env python3
""" Universal Blood Supply

A game by Asher Merrill for Ludum Dare 44.
"""

import math
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

        # Some time vars:
        self.ticks = 0
        self.time = 0

        # Define speed of game:
        self.vars['speed'] = 1.
        # Cost of living, (can be changed.) BY DEFAULT 1 MONEY PER SECOND:
        self.vars['upkeep'] = 3. / 720.
        # Starting money while here, used to keep currency later:
        self.vars['money']  = self.vars['max_money'] = 12.
        # Blood:
        self.vars['blood'] = 100.
        # Max blood, maybe for something vampiric...
        self.vars['blood_max'] = 100.
        # Regen rate:
        self.vars['blood_regen'] = 1./12.
        # Lastly the total sold:
        self.vars['blood_sold'] = 0
        # Blood to unit conversion ratio (ie., divide blood sold by this...):
        self.vars['blood_unit_conversion'] = 60
        # Get this percent going:
        self.vars['blood_character_percent'] = self.vars['blood'] / \
            self.vars['blood_max'] * 100
        # That should be all the initialization required...

        # Sell blood manual stuff:
        # How much blood blood is sold each time:
        self.vars['blood_sell_quantity'] = 60.
        # How much blood is sold for:
        self.vars['blood_sell_price'] = 24.
        # How much blood is stored:
        self.vars['blood_stored'] = 0

        # Some stuff about the economy:
        self.vars['economy_demand_terran_max_units'] = 5e12
        self.vars['economy_demand_terran'] = 0.25
        self.vars['economy_demand_modifiers'] = {'None_Null_modifier_example': "demand += 0"}

        # List of all researches and whether or not to allow them now:
        # Autosuck:
        self.Autosuck = False


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
            if self.ticks % 300 == 0:
                years, seconds = divmod(self.time, 365.2422 * 24 * 3600)
                weeks, seconds = divmod(seconds, 7 * 24 * 3600)
                days, seconds = divmod(seconds, 24 * 3600)
                hours, seconds = divmod(seconds, 3600)
                minutes, seconds = divmod(seconds, 60)
                self.vars['log'].append(f"Current game time is {int(years):d} years, {int(weeks):d} weeks, {int(days):d} days, {int(hours):d}:{int(minutes):d}:{round(seconds)}.")

    def update(self):
        """ Method to update current balances of things,
        (and other numbers as they become relevant.) """
        self.ticks += 1
        self.time += self.vars['speed'] / 60

        # Check to make sure we're alive:
        #FIXME
#        if self.vars['money'] <= 0 or self.vars['blood'] <= 0:
#            if self.vars['money'] < 0:
#                self.vars['money'] = 0
#            if self.vars['blood'] < 0:
#                self.vars['blood'] = 0
#            # Set state to dead if we are...
#            self.alive = False
#            if not elements['console_dead_notice'].active:
#                elements['console_dead_notice'].active = True

        # Do these if we're alive:
        if self.alive:
            # Do these first:
            if self.vars['money'] > self.vars['max_money']:
                self.vars['max_money'] = self.vars['money']  # Update max money
            # Subtract cost from money:
            self.vars['money'] -= self.vars['upkeep'] * self.vars['speed']
            # Add however much we've regened:
            if self.vars['blood'] < 100.:
                # Complicated regen expression following an approximately
                # logitic curve with sharp bottom at 0:
                # First set some QoL vars:
                y = self.vars['blood']
                # Now figure out how far up the curve we are, which dictates our regen:
                x = 1/(y - 100) * 3 * (-13 * y + -60 * ((y - 100)**2)**(1/3) + 1300)
#                print(x, y)
                # And define how many ticks_per_x there are:
                ticks_per_x = self.vars['speed']
                self.vars['blood'] += 100 - 1 / ((x + ticks_per_x + 39) / 180)**3 - (100 - 1 / ((x + 39) / 180)**3)

            # Regularly updated elements:
            # Elements from researches EVERY tick, (updateOn == "EVERY"):
            for _, l in research.items():
                if (l['class'].resType == 'AUTO' and
                    l['class'].active and
                    l['class'].updateOn == "EVERY"):
                    gameFunction = l['class'].gameFunctionName()
                    gameFunction(self)

            # Only do these every 1/10th second:
            if self.ticks % 6 == 0:
                # Check if we can enable any new researches:
                self.research_allow()

                # Process queue of researches and their effects:
                for _, l in research.items():
                    if (l['class'].resType == 'AUTO' and
                        l['class'].active and
                        l['class'].updateOn == "TICK"):
                        gameFunction = l['class'].gameFunctionName()
                        gameFunction(self)

            # Only do these when blood reaches is 0.95 * max:
            if self.vars['blood'] >= 0.95 * self.vars['blood_max']:
                for _, l in research.items():
                    if (l['class'].resType == 'AUTO' and
                        l['class'].active and
                        l['class'].updateOn == "BLOOD"):
                        gameFunction = l['class'].gameFunctionName()
                        gameFunction(self)

        # Finally update some things at the end here:
        # Get this percent going:
        self.vars['blood_character_percent'] = \
            self.vars['blood'] / \
            self.vars['blood_max'] * 100

    def update_display(self):
        """ Method to update the display. """
        pygame.display.update()
        CLOCK.tick(FPS)

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
                    if ((elem_obj.mouse_over(self.mouse)
                         if isinstance(elem_obj, (Container, Button))
                         else elem_obj.mouse_over())
                        and elem_obj.active):
                        # Lookup the game function, according to the type:
                        if isinstance(elem_obj, (Button, Text)):
                            gameFunction = elem_obj.gameFunctionName()
                        elif isinstance(elem_obj, Container):
                            gameFunction = \
                                elem_obj.gameFunctionName(self.mouse)
                if not gameFunction:
                    # Process entities in the research queue:
                    gameFunction = self.event_research_queue()
                # If we STILL don't have a function:
                if not gameFunction:
                    gameFunction = Game.event_null
                # Now call the game function:
                print(gameFunction)
                gameFunction(self)

    def event_null(self):
        """ A null event for the death notification, and possibly others... """
        pass

    def event_research_queue(self):
        """ Method to check if any research interactions occurred.

        Returns gameFunction from whatever button was depressed. """
        # Select what researches are unlocked and next in the queue:
        for j, v in enumerate([i for _, i in research.items() if i['class'].unlocked
                               and not i['class'].active][:3]):
            # Spoof mouse location so we can get buttons right:
            mouse = (self.mouse[0] - 1140, self.mouse[1] - 100 - (18 + 194 * j))
            # Ask if any of the buttons are active:
            for b in v['actions']:
                if b.mouse_over(mouse) and b.active:
                    # Lookup the game function, according to the type:
                    if isinstance(b, (Button, Text)):
                        gameFunction = b.gameFunctionName()
                    elif isinstance(b, Container):
                        gameFunction = b.gameFunctionName(mouse)
                    return gameFunction

    def event_console_speed_up(self):
        """ Console speed control functions. """
        if self.alive:
            if self.vars['speed'] < 10000.:
                self.vars['speed'] *= 1.2
                if self.vars['speed'] > 10000.:
                    self.vars['speed'] = 10000.

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
            self.vars['blood'] -= self.vars['blood_sell_quantity']
            self.vars['money'] += self.vars['blood_sell_price']
            self.vars['blood_sold'] += self.vars['blood_sell_quantity']

    def event_Scientific_BasicEconomics_handler(self):
        """ Method to call all the other functions that BasicEconomics
        relies on. """
        # Update demand:
        self.event_Scientific_BasicEconomics_demand()
        self.event_Scientific_BasicEconomics_store()


    def event_Scientific_BasicEconomics_demand(self):
        """ Method to determine the demand of the terran economy.

        I wanted a model that has:
            Primary behaviour like 1/x
            f(x) = 1 at x = 0
            f(x) = 0.1 at x = economy_demand_terran_max_units

        This yielded a model like:
            f(x) = a / (x + a)
            a = 5.555556e11

        I'm going to allow demand to be modified by things like marketing,
        etc, which will have exponentially decaying effects.

        These effects will be added to a list as expressions, which are
        evaluated here.
        """
        # The demand expression:
        a = 5.555556e11
        x = self.vars['blood_sold']
        demand =  - a / (x + a)**2

        # Evaluate all expressions:



    def event_Scientific_BasicEconomics_store(self):
        """ Method to manually sell blood. """
        if self.alive:
            self.vars['blood'] -= self.vars['blood_sell_quantity']
            self.vars['blood_stored'] += self.vars['blood_sell_quantity']

    def draw(self):
        """ Method to draw the screen each time a frame is requested. """
        # Handle some "constants", (ie., elements that always exist:)
        self.display.fill(WHITE)  # Always clear the display...
        self.draw_console()  # Update the console...
        self.draw_research_queue()  # Redraw the research queue...
        self.draw_character()  # Draw character...

        # Now draw the buttons:
        for elem_name, elem_obj in elements.items():
            # We need to only draw active objects and things that aren't
            # researches.  The research queue thing will handle researches.
            if elem_obj.active:
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
        disp_text_center_vertical(console,  # Health
                                  BOLDFONT,
                                  "HEALTH",
                                  RED,
                                  (1020, 34))
        disp_text_center_vertical(console,  # Money
                                  BOLDFONT,
                                  "MONEY",
                                  GOLD,
                                  (1020, 50))
        disp_text_center_vertical(console,  # Blood sold
                                  BOLDFONT,
                                  "UNITS SOLD",
                                  BLACK,
                                  (1020, 66))
        disp_text_center_vertical(console,  # Blood remaining
                                  FONT,
                                  "{:<40s}".format(str("*" *
                                   int(40 * self.vars['blood']
                                   / self.vars['blood_max']))),
                                  RED,
                                  (1105, 34))
        disp_text_center_vertical(console,  # Money
                                  FONT,
                                  "$" + f"{self.vars['money']:39.2f}",
                                  BLACK,
                                  (1105, 50))
        # Round off out units sold so it looks nice:
        units_sold = round(self.vars['blood_sold'] /
                           self.vars['blood_unit_conversion'])
        disp_text_center_vertical(console,  # Units of blood sold, total.
                                  FONT,
                                  f"{units_sold:40d}",
                                  BLACK,
                                  (1105, 66))

        # Finally blit display:
        self.display.blit(console, (0, 0))

    def draw_character(self):
        """ Method to draw and animate the character correctly. """
        character = pygame.Surface((300, 200))
        character.fill(GRAY_LIGHT)
        text = Text("The character will\n"
                    "go here with animations\n"
                    "correspondingto blood\n"
                    "percent: {blood_character_percent:5.2f}%.\n"
                    "12345678901234567890123456789012345678901234567890",
                    RED,
                    (0, 0),
                    font=FONT,
                    centerx=False,
                    centery=False)

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
        for j, v in enumerate([i for _, i in research.items() if i['class'].unlocked
                               and not i['class'].active][:3]):
            # Spoof mouse location so we can get buttons right:
            mouse = (self.mouse[0] - 1140, self.mouse[1] - 100 - (18 + 194 * j))
            # Create the techWindow from the tech's class:
            techWindow = v['class'].draw(mouse, self.vars)
            # Draw the buttons:
            for b in v['actions']:
                if b.active:
                    b.draw(techWindow, mouse)
            # Draw the tech window into the queue window:
            queue.blit(techWindow, (0, 18 + 194 * j))
        # Draw the queue window:
        self.display.blit(queue, (1140, 100))


    def draw_dead(self):
        """ Method to display scores and pause game. """

    def research_allow(self):
        """ Method that checks if new techs in each tree should be
        unlocked, AND if any mutually exclusive techs are used.

        (The latter bit is also accomplished in various Research.activate()
        methods.) """
        # Check all techs in research as see if we can unlock them:
        for _, v in research.items():
            if v['class'].allow_unlock(self.vars) == True:
                v['class'].unlocked = True

    def research_activate_Scientific_Hematology(self):
        """ Method to activate the Hematology research.

        Modify internal parameters and then call the Hematology class's
        activate method to finish the job.

        NOTE: By never changing the active status of Hematology to False,
        (and this is okay because it has no "live" parameters,) it's always
        ready to be displayed in the queue again, which is good. """
        # Find the correct instance of Hematology:
        v = research['Scientific_Hematology']

        # Update class vars from what Hematology says:
        self.vars['money'] -= Scientific_Hematology.base_cost * 2 ** v['class'].tech_num
        self.vars['upkeep'] *= Scientific_Hematology.upkeep_mult
        self.vars['blood_regen'] *= Scientific_Hematology.regen_mult
        # Increment the tech number:
        v['class'].tech_num += 1
        v['class'].unlocked = False
        # Leave Hematology "inactive," see above:
        # v['class'].active = False

    def research_activate_Scientific_BasicEconomics(self):
        """ Method to activate the BasicEconomics research. """
        # Get the instance of Scientific_BasicEconomics
        v = research['Scientific_BasicEconomics']

        # Update class vars from what Autosuck says:
        self.vars['money'] -= Scientific_BasicEconomics.base_cost
        # Adjust things so the tech doesn't come back:
        v['class'].active = True
        # Disable the research:
        v['class'].unlocked = True

        # Disable old sell button, and enable the new one:
        elements['sell_blood_manual_button'].active = False
        elements['sell_blood_manual_price'].active = False
        elements['research_Scientific_BasicEconomics_container'].active = True

    def research_activate_None_Autosuck(self):
        v = research['None_Autosuck']

        # Update class vars from what Autosuck says:
        self.vars['money'] -= None_Autosuck.base_cost
        self.vars['upkeep'] *= None_Autosuck.upkeep_mult
        # Enable Autosuck, and change state to active so
        # we know it's already occuring/it does occur.
        v['class'].active = True
        # Disable the research:
        v['class'].unlocked = True

    def research_Scientific_BasicEconomics_random_sell(self):
        """ Method to randomize selling blood at different prices. """
        pass

    def research_None_Autosuck(self):
        """ Method to manually subtract of multiple of (half manual amount)
        when blood is greater than 95 and will remain greater than 65. """
        # If we don't yet have basic economics/the ability to sell/store blood:
        if not research['Scientific_BasicEconomics']['class'].active:
            if self.vars['blood'] - 65 >= self.vars['blood_sell_quantity'] / 2:
                n = math.floor((self.vars['blood'] - 65) / \
                               (self.vars['blood_sell_quantity'] / 2))
            else:
                n = 0
            self.vars['blood'] -= n * self.vars['blood_sell_quantity'] / 2
            self.vars['money'] += n * self.vars['blood_sell_price'] / 2
            self.vars['blood_sold'] += n * self.vars['blood_sell_quantity'] / 2
        # If we do:
        else:
            if self.vars['blood'] - 65 >= self.vars['blood_sell_quantity'] / 2:
                    n = math.floor((self.vars['blood'] - 65) / \
                                   (self.vars['blood_sell_quantity'] / 2))
            else:
                n = 0
            self.vars['blood'] -= n * self.vars['blood_sell_quantity'] / 2
            self.vars['blood_stored'] += n * self.vars['blood_sell_quantity'] / 2

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
                              )) and i.mouse_over(mouse) and i.active:
                return True
            elif isinstance(i, Text) and i.active:  # Text
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
            if isinstance(i, Button) and i.active:
                i.draw(container, mouse)
            elif isinstance(i, Text) and i.active:
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
    def __init__(self, resType, unlocked=False, active=False,
                 gameFunction=None, updateOn='TICK'):
        """ Method to initialize generic research.

        There are two types of research: ONCLICK and AUTO, (all caps,
        as strings.)  ONCLICK can be something that changes numbers, (ie.,
        Hematology 0 through infinity,) or something that enables a Container
        and its associated actions.  AUTO is something that requires a game
        update, and is processed in Game.update.
        """
        # Make sure no one's being stupid, (ie., me):
        assert (resType == 'ONCLICK') or (resType == 'AUTO')
        self.resType = resType
        """ Is this a auto-repeating tech, (ie., Autosuck,) or an onclick tech,
        (ie., Hematology?) """
        # Now the regular params:
        """ Is the tech unlocked/can it be displayed to the user? """
        self.unlocked = unlocked
        """ Is the tech active, (ie., has it been researched?) """
        self.active = active
        """ If this is an ONCLICK tech that is repeating, how many times
        through? """
        self.tech_num = 0
        """  What function do we call? """
        self.gameFunction = gameFunction
        """ When do we need to call the gamefunction?

        BLOOD corresponds to Blood >= 0.95 * max;
        TICK corresponds to EVERY 6 TICKS, (NOT EVERY TICK);
        EVERY corresponds to EVERY tick.

        This parameter does nothing for entities that are resType != AUTO """
        assert updateOn in ["TICK", "EVERY", "BLOOD"]
        self.updateOn = updateOn

    def draw(self, mouse, fmtvars):
        """ Method to draw buttons and relevant text of tech. Returns a pygame
        surface that the caller will blit in the correct location. """
        techWindow = pygame.Surface((300, 194))
        techWindow.fill(GRAY_LIGHT)
        return techWindow

    def allow_unlock(self, fmtvars):
        """ Method to check if all conditions are valid to allow unlock. """

    def gameFunctionName(self):
        """ Method to return (upstream) the name of the function to be
        executed. """
        return self.gameFunction


class Scientific_Hematology(Research):
    """ A subclass of research.Opens Scientific branch:

        1. Increasing upkeep/cost (5%)
        2. Increase regen rate (30%) """
    """ Research Name """
    resName = "Hematology {} (Science)".upper()
    """ How much money to unlock this tech? """
    base_cost = 10.
    """ How much more upkeep does this cost? """
    upkeep_mult = 1.05
    """ How much more regen do we get? """
    regen_mult = 1.5

    # Create text string:
    #TODO: Update this list of strings to be nice.
    text = ["Purchase a hematology textbook for\n"\
            "${cost:6.2f} to learn how to eat better\n"\
            "and produce more blood. Increase\n"\
            "upkeep by {upkeep_mult:4.2f}x AND increase regen\n"\
            "by {regen_mult:4.2f}x."]

    def draw(self, mouse, fmtvars):
        """ Method to draw buttons and stuff.

        Returns a pygame surface that the caller will blit in the correct
        location. """
        # Create a pygame surface:
        techWindow = super(Scientific_Hematology, self).draw(mouse, fmtvars)
        # Draw a nice title:
        title = Text(Scientific_Hematology.resName.format(self.tech_num),
                     GRAY_DOWN,
                     (5, 5),
                     font=FONT,
                     centerx=False,
                     centery=False)
        title.draw(techWindow)

        # Create the text to throw into the research queue:
        text = Scientific_Hematology.text[self.tech_num if
                                          self.tech_num <
                                          len(Scientific_Hematology.text)
                                          else -1] \
        .format(**{'cost':Scientific_Hematology.base_cost * 2**self.tech_num,
                   'upkeep_mult':Scientific_Hematology.upkeep_mult,
                   'regen_mult':Scientific_Hematology.regen_mult})

        # Now the explanation of the tech:
        words = Text(text,
                     BLACK,
                     (10, 21),
                     font=FONT,
                     centerx=False,
                     centery=False)
        # ......the above is one (poorly readable) block.

        # Write that and return:
        words.draw(techWindow)
        return techWindow

    def allow_unlock(self, fmtvars):
        """ Method to check to make sure we have enough money over all time """
        if fmtvars['blood_sold'] / fmtvars['blood_unit_conversion'] >= \
        1.24336 * math.exp(0.693833*self.tech_num):
            return True
        else:
            return False


class Scientific_BasicEconomics(Research):
    """ A subclass of research. """
    """ Research Name """
    resName = "Basic Economics (Science)".upper()
    """ How much money to unlock this tech? """
    base_cost = 250.

    # Create text string:
    text = "Tired of being *the* dumb kid on\n"\
           "the block?  Show 'em all by\n"\
           "learning some high school (maybe\n"\
           "even middle school) economics!\n"\
           "You too can control the world\n"\
           "through numbers...\n"\
           "${:6.2f}"

    def draw(self, mouse, fmtvars):
        """ Method to draw buttons and stuff.

        Returns a pygame surface that the caller will blit in the correct
        location. """
        # Create a pygame surface:
        techWindow = super(Scientific_BasicEconomics, self).draw(mouse, fmtvars)
        # Draw a nice title:
        title = Text(Scientific_BasicEconomics.resName, GRAY_DOWN, (5, 5), font=FONT,
                     centerx=False, centery=False)
        title.draw(techWindow)

        # Now the explanation of the tech:
        words = Text(Scientific_BasicEconomics.text.format(Scientific_BasicEconomics.base_cost),
                     BLACK, (10, 21),
                     font=FONT,
                     centerx=False,
                     centery=False)
        words.draw(techWindow)
        return techWindow

    def allow_unlock(self, fmtvars):
        """ Method to check to make sure we have enough money over all time """
        if fmtvars['blood_sold'] / fmtvars['blood_unit_conversion'] > 1. and \
        fmtvars['max_money'] >= 2:
            return True
        else:
            return False

#TODO Make Autosuck respond to having basic economics, (ie., put stuff in storage.)
class None_Autosuck(Research):
    """ A subclass of research. """
    """ Research Name """
    resName = "Auto Bloodsuck".upper()
    """ How much money to unlock this tech? """
    base_cost = 500.
    upkeep_mult = 1.2

    # Create text string:
    text = "Autosuck® Homesucker™ brings the\n"\
           "convenience of your living\n"\
           "room to the profitability of\n"\
           "donating blood!  Homesucker™\n"\
           "removes half the normal amount the\n"\
           "normal amount of blood, allowing\n"\
           "you to do the rest. ${:6.2f}.\n"\
           "Upkeep increased by {:4.2f}x.\n"

    def draw(self, mouse, fmtvars):
        """ Method to draw buttons and stuff.

        Returns a pygame surface that the caller will blit in the correct
        location. """
        # Create a pygame surface:
        techWindow = super(None_Autosuck, self).draw(mouse, fmtvars)
        # Draw a nice title:
        title = Text(None_Autosuck.resName, GRAY_DOWN, (5, 5), font=FONT,
                     centerx=False, centery=False)
        title.draw(techWindow)

        # Now the explanation of the tech:
        words = Text(None_Autosuck.text.format(*[None_Autosuck.base_cost, None_Autosuck.upkeep_mult]),
                     BLACK, (10, 21),
                     font=FONT,
                     centerx=False,
                     centery=False)
        words.draw(techWindow)
        return techWindow

    def allow_unlock(self, fmtvars):
        """ Method to check to make sure we have enough money over all time """
        if fmtvars['blood_sold'] / fmtvars['blood_unit_conversion'] > 5.:
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
#        'test_container': Container(GRAY_LIGHT, (360, 250, 720, 400), [
#            Button(GRAY_UP, GRAY_DOWN, (10, 10, 100, 100), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
#            Button(GRAY_UP, GRAY_DOWN, (10, 210, 100, 100), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
#            Button(GRAY_UP, GRAY_DOWN, (210, 10, 100, 100), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
#            Button(GRAY_UP, GRAY_DOWN, (210, 210, 100, 100), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
#            Text("Text stuff... {blood}", RED, (410, 210, 100, 100), active=True, centerx=False, centery=False, human_name="test_container Blood Readout")
#            ], active=True),

        # Console entities:
        'console_dead_notice': Button(RED_UP, RED_UP, (220, 10, 780, 80), Game.event_null, active=False, text='!!! YOU ARE DEAD !!!'),
        'console_<<': Button(RED_UP, RED_DOWN, (25, 12, 50, 50), Game.event_console_speed_down, active=True, text='<<'),
        'console_==': Button(GRAY_UP, GRAY_DOWN, (85, 12, 50, 50), Game.event_console_speed_normal, active=True, text='=='),
        'console_>>': Button(GREEN_UP, GREEN_DOWN, (145, 12, 50, 50), Game.event_console_speed_up, active=True, text='>>'),

        # Game opening sell blood option:
        'sell_blood_manual_button': Button(GRAY_UP, GRAY_DOWN, (10, 110, 96, 32), Game.event_sell_blood_manual, active=True, text='Sell Blood'),
        'sell_blood_manual_price': Text('for ${blood_sell_price:6.2f}.', BLACK, (20 + 96, 110 + 16), font=FONT, active=True, centerx=False, centery=True),

        # Menus that become available when you can first sell blood:
        'research_Scientific_BasicEconomics_container': Container(GRAY_LIGHT, (10, 110, 285, 200), [
            Button(GRAY_UP, GRAY_DOWN, (10, 10, 120, 32), Game.event_Scientific_BasicEconomics_store, active=True, text='Harvest Blood', font=BOLDFONT),
            Text("Stored blood: {blood_stored:<10.4G}", BLACK, (10, 58), centerx=False, centery=True, active=True),
            Text("Blood per unit: {blood_unit_conversion:<d} per 1 unit.", BLACK, (10, 74), centerx=False, centery=True, active=True),
            Text("Selling blood for: ${blood_sell_price:0>6.2f}", BLACK, (10, 90), centerx=False, centery=True, active=True),
            Text("Public demand: {economy_demand_terran}%", BLACK, (10, 106), centerx=False, centery=True, active=True),


            #TODO: Fix this text
            # Text('for ${blood_sell_price:6.2f}.', BLACK, (20 + 96, 110 + 16), font=FONT, active=True, centerx=False, centery=True),
            ], active=False),
        }

""" Available research trees: """
treeScientific = ResearchTree()
treeSocial = ResearchTree()
treeSpiritual = ResearchTree()
treeNone = ResearchTree()


""" Research queue standard button positions. """
OK_LOWERRIGHT = (300 - 48 - 16, 194 - 32 - 16, 48, 32)

""" List of researches available in the game and their status. """
research = {
        # Hematology Tech
        "Scientific_Hematology": {'tree':treeScientific,
                                  'class':Scientific_Hematology('ONCLICK',
                                                                unlocked=False),
                                  'actions': [Button(GRAY_UP,
                                                     GRAY_DOWN,
                                                     OK_LOWERRIGHT,
                                                     Game.research_activate_Scientific_Hematology,
                                                     active=True,
                                                     text="OK")]},

        # Autosuck tech:
        "None_Autosuck":{'tree':treeNone,
                         'class':None_Autosuck('AUTO',
                                               unlocked=False,
                                               gameFunction=Game.research_None_Autosuck),
                         'actions': [Button(GRAY_UP,
                                            GRAY_DOWN,
                                            OK_LOWERRIGHT,
                                            Game.research_activate_None_Autosuck,
                                            active=True,
                                            text="OK")]},

        # BasicEconomics
        "Scientific_BasicEconomics":{'tree':treeScientific,
                                     'class':Scientific_BasicEconomics('AUTO',
                                                                       unlocked=False,
                                                                       gameFunction=Game.event_Scientific_BasicEconomics_handler),
                                     'actions': [Button(GRAY_UP,
                                                        GRAY_DOWN,
                                                        OK_LOWERRIGHT,
                                                        Game.research_activate_Scientific_BasicEconomics,
                                                        active=True,
                                                        text="OK")]},


        }


if __name__ == "__main__":
    g = Game()
    g.main()
