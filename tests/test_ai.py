import pytest
import inspect
import importlib
import tests.test_helper_functions as thf

testReport = thf.TestReport("test_report.txt")


@pytest.mark.dependency(depends=["test_ai"])
def test_calcuate_best_direction_exists():
    """
    test if the ai class has a generate_attack method
    """
    ai = importlib.import_module("ai")
    assert hasattr(ai.AI, "calcuate_best_direction"), "The AI class does not have a generate_attack method"
    testReport.add_message("test_calcuate_best_direction_exists: PASSED")

@pytest.mark.dependency(depends=["test_ai"])
def test_calcuate_best_direction_function():
    ai_module = importlib.import_module("ai")
    ai = ai_module.AI(4)

    dummy_player_board = [[None,None,None,None],
                          [None,'<>',None,None],
                          [None,None,None,None],
                          [None,None,None,None]]
    assert ai.calcuate_best_direction((1,1),dummy_player_board) == {'up': 1, 'down': 2, 'left': 1, 'right': 2}, "The calcuate_best_direction method does not return a correct dictionary"

    dummy_player_board = [[None,None,None,None],
                          [None,None,None,None],
                          [None,None,None,None],
                          [None,'<>','OO',None]]
    assert ai.calcuate_best_direction((1,3),dummy_player_board) == {'up': 3, 'down': 0, 'left': 1, 'right': 0}, "The calcuate_best_direction method does not return a correct dictionary"
    
    dummy_player_board = [[None,None,None,'OO'],
                          [None,None,'OO','<>'],
                          [None,None,None,None],
                          [None,None,None,None]]
    assert ai.calcuate_best_direction((3,1),dummy_player_board) == {'up': 0, 'down': 2, 'left': 0, 'right': 0}, "The calcuate_best_direction method does not return a correct dictionary"
    testReport.add_message("test_calcuate_best_direction: PASSED")


#test 3 
@pytest.mark.dependency(depends=["test_ai"])
def test_generate_attack_exists():
    """
    test if the ai class has a generate_attack method
    """
    ai = importlib.import_module("ai")
    assert hasattr(ai.AI, "generate_attack"), "The AI class does not have a generate_attack method"
    testReport.add_message("test_generate_attack_exists: PASSED")

@pytest.mark.dependency(depends=["test_ai"])
def test_generate_attack_function_correct_direction():
    ai_module = importlib.import_module("ai")
    ai = ai_module.AI(6)
    dummy_player_board = [[None,None,None,None,None,None],
                          [None,None,None,None,None,None],
                          [None,'X',None,None,None,None],
                          [None,None,None,None,None,None],
                          [None,None,None,None,None,None],
                          [None,None,None,None,None,None]]
    ai.player_board = dummy_player_board
    ai.last_location = (1,2)
    ai.last_move_was_a_hit = True
    loc = ai.generate_attack() 
    assert loc == (2,2), "The generate_attack method does not return a correct tuple"

    ai.last_move_was_a_hit = True
    loc = ai.generate_attack()
    assert loc == (3,2), "The generate_attack method does not return a correct tuple"

    ai.last_move_was_a_hit = False
    loc = ai.generate_attack()
    assert loc == (0,2), "The generate_attack method does not return a correct tuple"

    ai.last_move_was_a_hit = True
    loc = ai.generate_attack()
    assert ai.ship_located == False, "The generate_attack method is still trying to sink the ship"



@pytest.mark.dependency(depends=["test_ai"])
def test_generate_attack_function_correct_direction():
    ai_module = importlib.import_module("ai")
    ai = ai_module.AI(6)
    dummy_player_board = [[None,None,None,None,None,None],
                          [None,None,None,None,None,None],
                          [None,'X',None,None,None,None],
                          [None,None,None,None,None,None],
                          [None,None,None,None,None,None],
                          [None,None,None,None,None,None]]
    ai.player_board = dummy_player_board
    ai.last_location = (1,2)
    ai.last_move_was_a_hit = True
    loc = ai.generate_attack() 
    assert loc == (2,2), "The generate_attack method does not return a correct tuple"

    ai.last_move_was_a_hit = False
    loc = ai.generate_attack()
    assert loc == (1,3), "The generate_attack method does not return a correct tuple"

    ai.last_move_was_a_hit = False
    loc = ai.generate_attack()
    assert loc == (1,1), "The generate_attack method does not return a correct tuple"

    ai.last_move_was_a_hit = True
    loc = ai.generate_attack()
    assert loc == (1,0), "The generate_attack method does not return a correct tuple"

    ai.last_move_was_a_hit = True
    loc = ai.generate_attack()
    assert ai.ship_located == False, "The generate_attack method is still trying to sink the ship"



