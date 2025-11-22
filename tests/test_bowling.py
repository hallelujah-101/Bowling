import pytest 
from bowling.utils import Bowling 

def test_regular_roll_case():
    
    spare_strike_frames = [[2,3],[3,4],[1,0],[1,2],[3,3]]
    game = Bowling(spare_strike_frames)
    score = game.get_total_score() 
    
    assert score == 22

def test_spare_strike_case():
    
    spare_strike_frames = [[2,3],[4,6],[10],[1,2],[4,3]]
    game = Bowling(spare_strike_frames)
    score = game.get_total_score() 
    
    assert score == 48 
    
def test_strike_spare_case():
    
    spare_strike_frames = [[2,3],[10],[4,6],[1],[4,3]]
    game = Bowling(spare_strike_frames)
    score = game.get_total_score() 
    
    assert score == 44 
    

def test_strike_strike_case():
    
    spare_strike_frames = [[2,3],[10],[10],[1,2],[4,3]]
    game = Bowling(spare_strike_frames)
    score = game.get_total_score() 
    
    assert score == 49





