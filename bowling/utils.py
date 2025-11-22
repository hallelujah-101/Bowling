from typing import List
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

class Bowling:
    """
    A class that represents a bowling game
    """
    
    def __init__(self, frames: List[int], number_of_players: int = 2): 
        """Initializes a bowling game

        Args:
            frames (List[int]): List of scores per frame
            number_of_players (int, optional): The number of players in the game. Defaults to 2.
        """
        
        self.logger = logging.getLogger(__name__)
        
        self.frames = frames
        self.number_of_players = number_of_players
        
        self.scores: dict = {}
        self.points: dict = {}
        
        self.initialise_game_state(number_of_players)
        
        
    def initialise_game_state(self, number_of_players: int):
        """Initializes the state of a bowling game

        Args:
            number_of_players (int): the number of players in the game
        """
        
        for i in range(0, number_of_players):
            self.scores.update({i: 0})
            self.points.update({i: {'strike': [], 'spare': []}})
        
    def get_total_score(self) -> int:
        """Calculates the total score in the bowling game

        Returns:
            int: The total score from the game
        """
        
        try:
            index = 0
            player = 0
            frame_length = len(self.frames)
            
            while index < frame_length:
                if index != 0:
                    player = (player + 1) % (self.number_of_players)
                
                self.logger.debug(f'Player playing: Player {player}')
                
                new_index = self.play_turn(player ,index)
                    
                self.logger.debug(f'    The score for Player {player} is now: {self.scores[player]}')
                index = new_index
            
            total_score = sum(self.scores.values())
            self.logger.debug(f'Game complete with total score: {total_score}')
            return total_score
        except Exception as e:
            self.logger.error(e)
    
    
    def play_turn(self, player: int, frame_index: int) -> int:
        """Updates the state of the game for the player's turn and returns the frame for the next player starts

        Args:
            player (int): The current player
            frame_index (int): The frame the player started playing from

        Returns:
            int: The frame at which the player stops playing
        """
                
        frames = self.frames
        frames_length = len(self.frames)
        index = frame_index
        
        last_state = None
        start = True
        while (start == True or self.strike_or_spare(player) == True) and index < frames_length:
            # print(index)
            start = False
            
            frame = frames[index]
            frame_length = len(frame)
            frame_points = sum(frame)

            had_strike_spare = self.strike_or_spare(player)
            # print("Try to complete frame")
            self.try_complete_frames(player, frame)
            # print("Frame completed")

            if self.is_strike(frame_points, frame_length):
                self.points[player]['strike'].append(frame)
                last_state = 0  
            elif self.is_spare(frame_points, frame_length):
                if last_state == 1:
                    raise Exception(f'The size of the frame: {frame} at index: {index} is {frame_length}. This is not allowed after a spare, check data for expected singular frame.')
                    
                self.points[player]['spare'].append([10])
                last_state = 1              
            
            if self.strike_or_spare(player) == False:
                self.scores[player] += frame_points
                self.logger.debug(f'    The score for the player after frame {index} is: {self.scores[player]}')
                self.logger.debug(f'    The points for the player after frame {index} is: {self.points[player]}')
                index += 1
                break
                
            self.logger.debug(f'    The score for the player after frame {index} is: {self.scores[player]}')
            self.logger.debug(f'    The points for the player after frame {index} is: {self.points[player]}')
            index += 1
        
        if self.strike_or_spare(player) == True:
            self.scores[player] += self.get_pending_scores(player)
            self.logger.debug(f'    The score for the player after frame {index} is: {self.scores[player]}')
            self.logger.debug(f'    The points for the player after frame {index} is: {self.points[player]}')
            
        return index
    
    
    def get_pending_scores(self, player: int) -> int:
        """Gets all points from pending strike/spare calculations

        Args:
            player (int): The current player

        Returns:
            int: The total points from all pending calculations
        """
        
        pending_spares = sum([sum(spare) for spare in self.points[player]['spare']])
        pending_strikes = sum([sum(strike) for strike in self.points[player]['strike']])
        
        return (pending_spares + pending_strikes)
        
    def strike_or_spare(self, player: int) -> bool:
        """Checks whether the player has a pending strike and/or spare frames

        Args:
            player (int): The current player

        Returns:
            bool: Whether the player has pending strike and/or spare frames
        """
        
        if(any([state for state in self.points[player].keys() if self.points[player][state] != []])):
            return True
        
        return False
            
    
    def try_complete_frames(self, player: int, frame: int):
        """Iterates through the frames to complete any pending frame score calculations

        Args:
            player (int): The current player
            frame (int): The current frame 
        """
        
        for point in frame:
            self.complete_typed_frames(player, point, 3)
            self.complete_typed_frames(player, point, 2)
    
    def complete_typed_frames(self, player: int, point: int, frame_size: int):
        """
        Iterates through frames with pending score calculations which may 
        be from a prior 'strike' or 'spare' 

        Args:
            player (int): The current player
            point (int): The points gained from a roll
            frame_size (int): The number of rolls needed to complete a pending frame score calculation
        """
        
        frame_type = None
        if frame_size == 2:
            frame_type = 'spare'
        elif frame_size == 3:
            frame_type = 'strike'
            
        #print(f"Starting frame completion for {frame_type}s")
        
        frames = self.points[player][frame_type]
        
        #print(f"Current frames: {frames}")
        index = 0
        while index < len(frames):            
            frame = frames[index]
            frame_length = len(frame)
            
            #print(f"Current frames: {frames}")
            if frame_length < frame_size:
                frame.append(point)
                
                if len(frame) == frame_size:
                    self.scores[player] += sum(frame)
                    del self.points[player][frame_type][index]
                else:
                    index += 1
            
            #print(f"Current frames: {frames}")
            index += 1
                        

    def is_strike(self, frame_sum:int, frame_length: int) -> bool:
        """Checks if a player scored a strike in the frame

        Args:
            frame_sum (int): The sum of points in the frame
            frame_length (int): The number of balls a player used in the frame

        Returns:
            bool: Whether the player got a strike
        """
        
        if frame_length == 1 and frame_sum == 10:
            return True 
        
        return False 

    def is_spare(self, frame_sum: int, frame_length: int) -> bool:
        """Checks if a player scored a spare in the frame

        Args:
            frame_sum (int): The sum of points in the frame
            frame_length (int): The number of balls a player used in the frame

        Returns:
            bool: Whether the player got a spare
        """
        
        if frame_length == 2 and frame_sum == 10:
            return True
        
        return False

spare_strike_frames = [[2,3],[4,6],[10],[1,2],[4,3]]
game = Bowling(spare_strike_frames)
score = game.get_total_score()