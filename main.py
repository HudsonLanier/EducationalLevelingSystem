from random import choice

#generic prompts text is where users can put things that they would like to be asked to do.
#Here, they are called by a level and a number so that if you are testing the program, you can see what level you are on
#and what number prompt is being asked
generic_prompts_text = [
    ['Level1 Prompt 1', 'Level1 Prompt 2', 'Level1 Prompt 3'],
    ['Level 2 Prompt 1', 'Level 2 Prompt 2', 'Level 2 Prompt 3']
]

#each prompt in the generic_prompts_text will be instantiated into the Prompt_Status class in order to be able to
#track whether the prompt has been completed or not
class Prompt_Status:
    def __init__(self, prompt_text):
        self.prompt_text=prompt_text
        self.completed = False


#This function takes all of the generic prompts and instantiates them into the Prompt_Status class,
#returning a new list of prompts that are all instances of that class
def instantiate_prompts(list_of_list_of_prompts):
    local_list = list_of_list_of_prompts[:]
    new_list = []
    i = 0
    while i < len(local_list):
        new_list.append([])
        for value in local_list[i]:
            new_list[i].append(Prompt_Status(value))
        i += 1
    return  new_list

#this class is for defining pieces of music. Some of the information is helpful to have so that you know which piece
# you are referring too (title, composer, publication_year). Other information in this class helps the program know
# how far you've progressed (piece_level, list_of_phrases).

class Piece:
    def __init__(self, title, composer, publication_year, concert_tempo, star_bars, number_of_measures, piece_level=1):
        self.title = title
        self.composer = composer
        self.publication_year = publication_year
        self.concert_tempo = concert_tempo
        self.star_bars = star_bars
        self.number_of_measures = number_of_measures
        self.piece_level = piece_level
        self.list_of_phrases = []

    #The piece starts with an empty list_of_phrases,
    # and you add phrases to it using the add_phrase method.
    def add_phrase(self, start_measure, end_measure, phrase_number):
        self.list_of_phrases.append(Phrase(start_measure, end_measure, phrase_number, phrase_level=1))

    #the piece_level_up function checks to see if all of the phrases for a piece have been completed for the current
    #level. If the level of all of the phrases is greater than the level of the piece (meaning that they have all
    # been completed), the level of the piece is augmented by 1
    def piece_level_up(self):
        n = 0
        for phrase in self.list_of_phrases:
            if phrase.phrase_level > self.piece_level:
                n += 1
        if n == len(self.list_of_phrases):
            self.piece_level += 1
        else:
            pass


class Phrase(Piece):
    def __init__(self, start_measure, end_measure, phrase_number, phrase_level, piece):
        self.start_measure = start_measure
        self.end_measure = end_measure
        self.phrase_number = phrase_number
        self.phrase_level = phrase_level
        self.generic_prompts_text = generic_prompts_text
        self.phrase_prompts = instantiate_prompts(generic_prompts_text)
        self.piece = piece

    #when all of the prompts for a phrase are completed correctly, the level of that prompt is raised by 1
    def phrase_level_up(self):

        list_of_incomplete_prompts = []
        for prompt in self.phrase_prompts[(self.phrase_level - 1)]:
            if prompt.completed == False:
                list_of_incomplete_prompts.append(prompt)

        if len(list_of_incomplete_prompts) > 0:
            for incomplete_prompt in list_of_incomplete_prompts:

                if incomplete_prompt.completed == True:
                    list_of_incomplete_prompts.remove(incomplete_prompt)
                else:
                    print('for phrase {}'.format(self.phrase_number))
                    test_a_prompt(incomplete_prompt)

        elif len(list_of_incomplete_prompts) == 0:
            self.phrase_level += 1

#this function choses a phrase that has not been completed yet at the current level of progress in the learning of the
#piece
def select_a_phrase(some_piece):
    possible_choices = []
    for phrase in some_piece.list_of_phrases:
        if phrase.phrase_level == some_piece.piece_level:
            possible_choices.append(phrase)
        else:
            pass
    selected_phrase = choice(possible_choices)
    return selected_phrase


#display the prompt text and ask the user five times if they got it right. If you get 5 y answers, change the prom
#prompt to complete. If you get any other result, keep it as incomplete
def test_a_prompt(prompt_to_test):

    list_of_answers = []
    i = 0

    while i < 5:
        answer = str(input("did you {}".format(prompt_to_test.prompt_text)))
        list_of_answers.append(answer)
        i += 1
    if list_of_answers == ['y', 'y', 'y', 'y', 'y']:
        prompt_to_test.completed = True
    elif list_of_answers != ['y', 'y', 'y', 'y', 'y']:
        pass

#this function assesses if the phrase needs to be completed at the current level of the piece. If it does, then
#the user will be prompted to practice that phrase
def practice_all_phrases(list_of_phrases):
    for phrase in list_of_phrases:
        if phrase.phrase_level == phrase.piece.piece_level:
            phrase.phrase_level_up()


#this is an example of how a piece of music (in this case, Don Juan) would be created
Don_Juan = Piece('Don Juan', 'Strauss', 1885, 150, '6 through 15', 32, 1)

#here, we define the phrases in the Don Juan Piece
phrases_in_excerpt = [Phrase(1, 8, 1, 1, Don_Juan),
                      Phrase(9, 16, 2, 1, Don_Juan),
                      Phrase(17, 24, 3, 1, Don_Juan),
                      Phrase(25, 32, 4, 1, Don_Juan)]

#and here we assign those phrases to the piece so that they can be practiced
Don_Juan.list_of_phrases = phrases_in_excerpt

#this function is the master function of the program. Once the user has defined a Piece and a list of phrases for
#that piece, this function can be called with those two pieces of information as arguments and the trainer will run
def learn_all_phrases(piece, list_of_phrases):
    while list_of_phrases[0].piece.piece_level < 3:
        practice_all_phrases(list_of_phrases)
        piece.piece_level_up()

    print('this concludes the training')

#as an example, when this program is run, the prompts for Don Juan will be asked to the user of the program
learn_all_phrases(Don_Juan, Don_Juan.list_of_phrases)
