from bakery import assert_equal
from dataclasses import dataclass
from drafter import *

hide_debug_information()
set_website_title("Weighted Decision Matrix Calculator")
set_website_framed(False)
set_site_information(author="", description="", sources=["", ""], planning=[], links=[], server=None)

set_website_style("terminal")

@dataclass
class Option:
    name: str
    scores: list[int]
    total_score: float
    
@dataclass
class Criterion:
    name: str
    weight: int
    
@dataclass
class State:
    message: str
    options: list[Option]
    criteria: list[Criterion]
    winner: str
    
INTRODUCTION = """A decision matrix is a mathematical way of deciding between multiple complex options.
                  They are often used in processes like engineering design and product development, but
                  can be used for any complicated decision. A weighted decision matrix uses weighted
                  criteria, where each aspect of an option has a varying importance in the final outcome,
                  to provide a total score for each option that will help you determine the best decision
                  to take. Click the button below to get started."""

NAMING_OPTIONS = """Name all of the options that you are deciding between. Select the amount of options
                    that you want to name (up to 5) before inputing their names."""

NAMING_CRITERIA = """Name the criteria that you will use to make your decision. What qualities do you want
                     the winning option to have? Select the amount of criteria (up to 5) before inputing
                     their names."""

WEIGHING_CRITERIA = """Select weights for your criteria. A weight represents how important the criterion is
                       for your decision process. In this decision matrix, weights are represented by
                       percentages of 100, so be sure to only input numbers from 1-99. Your weights should
                       add up to 100."""

SCORING_OPTIONS = """Now score each of your options against each criterion, on a scale of 1-10 (1 being
                     the least aligned with the criteria and 10 being the most). Click 'Next' to score
                     the next option."""

def apply_weight(weight: int, score: int) -> float:
    converted_weight = weight / 100
    return score * converted_weight

def calculate_option(option: Option, criteria: list[Criterion]) -> float:
    weighted_scores = []
    for index, criterion in enumerate(criteria):
        weighted_scores.append(apply_weight(criterion.weight, option.scores[index]))
        
    total = 0.0
    for score in weighted_scores:
        total = total + score
    
    return total

assert_equal(calculate_option(Option("Red", [2, 3, 4, 5, 6], 0.0),
                              [Criterion("A color", 25),
                               Criterion("Nice", 25),
                               Criterion("Unique", 50)]), 3.25)

@route
def index(state: State) -> Page:
    return Page(state, [
         Header("Weighted Decision Matrix Calculator"),
         Paragraph(state.message),
         Button("Start a New Decision Matrix", "name_options")
         ])

@route
def name_options(state: State) -> Page:
    state.message = NAMING_OPTIONS
    
    textboxes = []
    for index, option in enumerate(state.options):
        textboxes.append("\nOption " + str(index+1) + ":")
        textboxes.append(TextBox("option_" + str(index+1), state.options[index].name))
        
    content = []
    content.append(state.message)
    for item in textboxes:
        content.append(item)
    content.append("\n")
    content.append(Button("Add Option", "add_option"))
    content.append(Button("Next", "save_options"))
        
    return Page(state, content)
                   
@route
def add_option(state: State) -> Page:
    if len(state.options) >=5:
        return name_options(state)
    state.options.append(Option("", [0, 0, 0, 0, 0], 0.0))
    return name_options(state)

@route
def save_options(state: State, option_1: str, option_2: str, option_3: str ="", option_4: str="", option_5: str="") -> Page:
    for index, option in enumerate(state.options):
        if index == 0:
            option.name = option_1
        elif index == 1:
            option.name = option_2
        elif index == 2:
            option.name = option_3
        elif index == 3:
            option.name = option_4
        elif index == 4:
            option.name = option_5
            
    return name_criteria(state)

@route
def name_criteria(state: State) -> Page:
    state.message = NAMING_CRITERIA
    
    textboxes = []
    for index, criterion in enumerate(state.criteria):
        textboxes.append("\nCriterion " + str(index+1) + ":")
        textboxes.append(TextBox("criterion_" + str(index+1), state.criteria[index].name))
        
    content = []
    content.append(state.message)
    for item in textboxes:
        content.append(item)
    content.append("\n")
    content.append(Button("Add Criterion", "add_criterion"))
    content.append(Button("Next", "save_criteria"))
    
    return Page(state, content)

@route
def add_criterion(state: State) -> Page:
    if len(state.criteria) >=5:
        return name_criteria(state)
    state.criteria.append(Criterion("", 0))
    return name_criteria(state)

@route
def save_criteria(state: State, criterion_1: str, criterion_2: str, criterion_3: str ="", criterion_4: str="", criterion_5: str="") -> Page:
    for index, criterion in enumerate(state.criteria):
        if index == 0:
            criterion.name = criterion_1
        elif index == 1:
            criterion.name = criterion_2
        elif index == 2:
            criterion.name = criterion_3
        elif index == 3:
            criterion.name = criterion_4
        elif index == 4:
            criterion.name = criterion_5
            
    return weigh_criteria(state)
    
@route
def weigh_criteria(state: State) -> Page:
    state.message = WEIGHING_CRITERIA
    
    textboxes = []
    for index, criterion in enumerate(state.criteria):
        textboxes.append(criterion.name + ":")
        textboxes.append(TextBox("weight_" + str(index+1), criterion.weight))
        textboxes.append("%")
        textboxes.append("\n")
        
    content = []
    content.append(state.message)
    content.append("\n")
    for item in textboxes:
        content.append(item)
    content.append(Button("Next", "save_weights"))
        
    return Page(state, content)

@route
def save_weights(state: State, weight_1: str, weight_2: str, weight_3: str="", weight_4: str="", weight_5: str="") -> Page:   
    for index, criterion in enumerate(state.criteria):
        if index == 0:
            criterion.weight = int(weight_1)
        elif index == 1:
            criterion.weight = int(weight_2)
        elif index == 2:
            criterion.weight = int(weight_3)
        elif index == 3:
            criterion.weight = int(weight_4)
        elif index == 4:
            criterion.weight = int(weight_5)

    return score_options(state, 0)

@route
def score_options(state: State, options_index: int) -> Page:
    state.message = SCORING_OPTIONS
    
    content = []
    content.append(state.message)
    content.append("\n")
    content.append("\n")
    content.append(bold(state.options[options_index].name))
    for index, criterion in enumerate(state.criteria):
        if index == 0:
            content.append("\n"+criterion.name+" ("+str(criterion.weight)+"%) :")
            content.append(TextBox("score_"+str(index+1),
                                   state.options[options_index].scores[index]))
        elif index == 1:
            content.append("\n"+criterion.name+" ("+str(criterion.weight)+"%) :")
            content.append(TextBox("score_"+str(index+1),
                                   state.options[options_index].scores[index]))
        elif index == 2:
            content.append("\n"+criterion.name+" ("+str(criterion.weight)+"%) :")
            content.append(TextBox("score_"+str(index+1),
                                   state.options[options_index].scores[index]))
        elif index == 3:
            content.append("\n"+criterion.name+" ("+str(criterion.weight)+"%) :")
            content.append(TextBox("score_"+str(index+1),
                                   state.options[options_index].scores[index]))
        elif index == 4:
            content.append("\n"+criterion.name+" ("+str(criterion.weight)+"%) :")
            content.append(TextBox("score_"+str(index+1),
                                   state.options[options_index].scores[index]))
    content.append("\n")
    content.append(Button("Next", "save_scores"))
    return Page(state, content)

@route
def save_scores(state: State, score_1: str, score_2: str, score_3: str="", score_4: str="", score_5: str="") -> Page:       
    if state.options[0].scores[0] == 0:
        options_index = 1
        for index, criterion in enumerate(state.criteria):
            if index == 0:
                state.options[0].scores[0] = int(score_1)
            elif index == 1:
                state.options[0].scores[1] = int(score_2)
            elif index == 2:
                state.options[0].scores[2] = int(score_3)
            elif index == 3:
                state.options[0].scores[3] = int(score_4)
            elif index == 4:
                state.options[0].scores[4] = int(score_5)
    elif state.options[1].scores[0] == 0 and len(state.options) == 2:
        for index, criterion in enumerate(state.criteria):
            if index == 0:
                state.options[1].scores[0] = int(score_1)
            elif index == 1:
                state.options[1].scores[1] = int(score_2)
            elif index == 2:
                state.options[1].scores[2] = int(score_3)
            elif index == 3:
                state.options[1].scores[3] = int(score_4)
            elif index == 4:
                state.options[1].scores[4] = int(score_5)
        return process_scores(state)
    elif state.options[1].scores[0] == 0 and len(state.options) > 2:
        options_index = 2
        for index, criterion in enumerate(state.criteria):
            if index == 0:
                state.options[1].scores[0] = int(score_1)
            elif index == 1:
                state.options[1].scores[1] = int(score_2)
            elif index == 2:
                state.options[1].scores[2] = int(score_3)
            elif index == 3:
                state.options[1].scores[3] = int(score_4)
            elif index == 4:
                state.options[1].scores[4] = int(score_5)
    elif state.options[2].scores[0] == 0 and len(state.options) == 3:
        for index, criterion in enumerate(state.criteria):
            if index == 0:
                state.options[2].scores[0] = int(score_1)
            elif index == 1:
                state.options[2].scores[1] = int(score_2)
            elif index == 2:
                state.options[2].scores[2] = int(score_3)
            elif index == 3:
                state.options[2].scores[3] = int(score_4)
            elif index == 4:
                state.options[2].scores[4] = int(score_5)
        return process_scores(state)
    elif state.options[2].scores[0] == 0 and len(state.options) > 3:
        options_index = 3
        for index, criterion in enumerate(state.criteria):
            if index == 0:
                state.options[2].scores[0] = int(score_1)
            elif index == 1:
                state.options[2].scores[1] = int(score_2)
            elif index == 2:
                state.options[2].scores[2] = int(score_3)
            elif index == 3:
                state.options[2].scores[3] = int(score_4)
            elif index == 4:
                state.options[2].scores[4] = int(score_5)
    elif state.options[3].scores[0] == 0 and len(state.options) == 4:
        for index, criterion in enumerate(state.criteria):
            if index == 0:
                state.options[3].scores[0] = int(score_1)
            elif index == 1:
                state.options[3].scores[1] = int(score_2)
            elif index == 2:
                state.options[3].scores[2] = int(score_3)
            elif index == 3:
                state.options[3].scores[3] = int(score_4)
            elif index == 4:
                state.options[3].scores[4] = int(score_5)
        return process_scores(state)
    elif state.options[3].scores[0] == 0 and len(state.options) > 4:
        options_index = 4
        for index, criterion in enumerate(state.criteria):
            if index == 0:
                state.options[3].scores[0] = int(score_1)
            elif index == 1:
                state.options[3].scores[1] = int(score_2)
            elif index == 2:
                state.options[3].scores[2] = int(score_3)
            elif index == 3:
                state.options[3].scores[3] = int(score_4)
            elif index == 4:
                state.options[3].scores[4] = int(score_5)
    elif state.options[4].scores[0] == 0 and len(state.options) == 5:
        for index, criterion in enumerate(state.criteria):
            if index == 0:
                state.options[4].scores[0] = int(score_1)
            elif index == 1:
                state.options[4].scores[1] = int(score_2)
            elif index == 2:
                state.options[4].scores[2] = int(score_3)
            elif index == 3:
                state.options[4].scores[3] = int(score_4)
            elif index == 4:
                state.options[1].scores[4] = int(score_5)
        return process_scores(state)
    print(state.options)
    return score_options(state, options_index)

@route
def process_scores(state: State) -> Page:
    for option in state.options:
        option.total_score = round(calculate_option(option, state.criteria), 2)

    maximum = state.options[0].total_score
    winner = state.options[0].name
    for option in state.options:
        if option.total_score >= maximum:
            maximum = option.total_score
            winner = option.name
            
    content = []
    content.append("The winner is " + winner + "! Check the results for ties.")
    content.append("\n")
    content.append("\nResults:")
    for option in state.options:
        content.append("\n"+option.name+" scored "+str(option.total_score))
    content.append("\n")
    content.append(Button("Score Again", "reset_option_scores"))
    content.append(Button("Start a New Decision Matrix", "reset_state"))
    return Page(state, content)

@route
def reset_option_scores(state: State) -> Page:
    for option in state.options:
        option.scores = [0, 0, 0, 0, 0]
    return score_options(state, 0)

@route
def reset_state(state: State) -> Page:
    state = State(NAMING_OPTIONS,
                   [Option("", [0, 0, 0, 0, 0], 0.0), Option("", [0, 0, 0, 0, 0], 0.0)],
                   [Criterion("", 0), Criterion("", 0)],
                   "")
    return name_options(state)

start_server(State(INTRODUCTION,
                   [Option("", [0, 0, 0, 0, 0], 0.0), Option("", [0, 0, 0, 0, 0], 0.0)],
                   [Criterion("", 0), Criterion("", 0)],
                   ""))
