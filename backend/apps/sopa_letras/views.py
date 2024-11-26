from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
import re

_WORD_SEARCH_LEN = 196
_MAX_ROW_LEN = 13
_MIN_ROW_LEN = 0

class wordSearch(APIView):    
    def post (self, request):

        letters, words = self.format_letter_words(request.data.get('letters'), request.data.get('words'))

        word_search = [letters[i:i+14] for i in range(0, len(letters), 14)]

        result = self.search_words(word_search, words)

        return Response(result, status=status.HTTP_200_OK)

    def format_letter_words(self, letter, words):

        letters_array = list(re.sub(r'[^a-zA-Z]', '', letter).upper())
        words_array = [word.upper() for word in re.findall(r'\b[a-zA-Z]+\b', words)]

        if len(letters_array) != _WORD_SEARCH_LEN:
            raise ValidationError({'message': f'la cantidad de letras debe ser igual a 196 caracteres. letras actuales: {len(letters_array)}'})

        return letters_array, words_array
    
    def search_words(self, word_search, words):

        result = []

        message = ''

        for word in words:

            for row, index in enumerate(word_search):

                if word[0] in index:

                    position = [i for i, value in enumerate(index) if value == word[0]]

                    message = self.search(row, position, word, index, word_search)

                    if message:
                        result.append(message)
                        break
            
            if not message:
                result.append(f'La palabra {word} no fue encontrada')

        return result
    
    def search(self, row, position, word, index, word_search):

        message = ''

        message = self.search_horizontal(index, word, row)

        if message: 
            return message

        message = self.search_vertical(word, row, position, word_search)

        if message:
            return message

        message = self.search_diagonal(word, row, position, word_search)

        if message:
            return message

    def search_horizontal(self, index, word, row):

        msg = 'la palabra {} existe en la fila {}'

        str_index = "".join(index)

        if word in str_index:
            return msg.format(word, row)
        
        if word in str_index[::-1]:
            return msg.format(word, row)
        
        return None

    def search_vertical(self, word, row, positions, word_search):

        build_word = ''
        msg = 'Vertical: la palabra {} existe desde la fila {} hasta la fila {}, en la posicion {}.'

        if (row + len(word)) <= _MAX_ROW_LEN:

            for position in positions:
                build_word = ''

                for i, value in enumerate(word):

                    if value != word_search[i][position]:
                        break

                    build_word += value

                if word == build_word:
                    return msg.format(word, row + 1, row + len(word), position + 1)

        if ((row + 1) - len(word) >= _MIN_ROW_LEN):
            
            for position in positions:
                build_word = ''

                for i, value in enumerate(word):

                    if value != word_search[row - i][position]:
                        break

                    build_word += value

                if word == build_word:
                    return msg.format(word, row + 1, (row + 1) - len(word), position + 1)

    def search_diagonal(self, word, row, positions, word_search):
        
        build_word = ''
        msg = 'Diagonal: La palabra {} inica en ({}, {}) y finaliza en ({}, {})'

        if (row + len(word)) <= _MAX_ROW_LEN:

            for position in positions:
                build_word = ''

                if (position + len(word)) <= _MAX_ROW_LEN:
                    
                    for i, value in enumerate(word):

                        if value != word_search[row + i][position + i]:
                            break

                        build_word += value

                    if word == build_word:
                        return msg.format(word, row + 1, position + 1, (row + 1) + len(word), (position + 1) + len(word))

                if ((position + 1) - len(word)) >= _MIN_ROW_LEN:

                    for i, value in enumerate(word):

                        if value != word_search[row + i][position - i]:
                            break

                        build_word += value

                    if word == build_word:
                        return msg.format(word, row + 1, position + 1, (row + 1) + len(word), (position + 1) - len(word))

        if ((row + 1) - len(word) >= _MIN_ROW_LEN):

            for position in positions:

                if ((position + 1) - len(word)) >= _MIN_ROW_LEN:

                    for i, value in enumerate(word):

                        if value != word_search[row - i][position - i]:
                            break

                        build_word += value

                    if word == build_word:
                        return msg.format(word, row + 1, position + 1, (row + 1) - len(word), (position + 1) - len(word))

                if (position + len(word)) <= _MAX_ROW_LEN:
                    for i, value in enumerate(word):

                        if value != word_search[row - i][position + i]:
                            break

                        build_word += value

                    if word == build_word:
                        return msg.format(word, row + 1, position + 1, (row + 1) - len(word), (position + 1) + len(word))
