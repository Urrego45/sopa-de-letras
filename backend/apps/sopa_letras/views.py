from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
import re

import pprint

class pruebaApi(APIView):    
    def post (self, request):

        letters, words = self.format_letter_words(request.data.get('letters'), request.data.get('words'))

        word_search = [letters[i:i+14] for i in range(0, len(letters), 14)]

        result = self.send_words(word_search, words)

        return Response(result, status=status.HTTP_200_OK)

    def format_letter_words(self, letter, words):

        letters_array = list(re.sub(r'[^a-zA-Z]', '', letter).upper())
        words_array = [word.lower() for word in re.findall(r'\b[a-zA-Z]+\b', words)]

        if len(letters_array) is not 196:
            raise ValidationError({'message': f'la cantidad de letras debe ser igual a 196 caracteres. letras actuales: {len(letters_array)}'})

        return letters_array, words_array
    
    def send_words(self, word_search, words):

        result = []

        message = ''

        for word in words:

            upper_word = word.upper()

            for row, index in enumerate(word_search):

                if upper_word[0] in index:

                    position = [i for i, value in enumerate(index) if value == upper_word[0]]

                    message = self.send(row, position, upper_word, index, word_search)

                    if message:
                        result.append(message)
                        break
            
            if not message:
                result.append(f'La palabra {upper_word} no fue encontrada')

        return result
    
    def send(self, row, position, word, index, word_search):

        message = ''

        message = self.send_horizontal(index, word, row)

        if message: 
            return message

        message = self.send_vertical(index, word, row, position, word_search)

        if message:
            return message

        message = self.send_diagonal(index, word, row, position, word_search)

        if message:
            return message


    def send_horizontal(self, index, word, row):

        msg = 'la palabra {} existe en la fila {}'

        str_index = "".join(index)

        if word in str_index:
            return msg.format(word, row)
        
        if word in str_index[::-1]:
            return msg.format(word, row)
        
        return None

    def send_vertical(self, index, word, row, positions, word_search):

        build_word = ''
        msg = 'Vertical: la palabra {} existe desde la fila {} hasta la fila {}, en la posicion {}.'

        if (row + len(word)) <= 13:

            for position in positions:
                build_word = ''

                for i, value in enumerate(word):

                    if value is not word_search[i][position]:
                        break

                    build_word += value

                if word == build_word:
                    return msg.format(word, row + 1, row + len(word), position + 1)

        if ((row + 1) - len(word) >= 0):
            
            for position in positions:
                build_word = ''

                for i, value in enumerate(word):

                    if value is not word_search[row - i][position]:
                        break

                    build_word += value

                if word == build_word:
                    return msg.format(word, row + 1, (row + 1) - len(word), position + 1)

    def send_diagonal(self, index, word, row, positions, word_search):
        
        build_word = ''
        msg = 'Diagonal: La palabra {} inica en ({}, {}) y finaliza en ({}, {})'

        if (row + len(word)) <= 13:

            for position in positions:
                build_word = ''

                if (position + len(word)) <= 13:
                    
                    for i, value in enumerate(word):

                        if value is not word_search[row + i][position + i]:
                            break

                        build_word += value

                    if word == build_word:
                        return msg.format(word, row + 1, position + 1, (row + 1) + len(word), (position + 1) + len(word))

                if ((position + 1) - len(word)) >= 0:

                    for i, value in enumerate(word):

                        if value is not word_search[row + i][position - i]:
                            break

                        build_word += value

                    if word == build_word:
                        return msg.format(word, row + 1, position + 1, (row + 1) + len(word), (position + 1) - len(word))

        if ((row + 1) - len(word) >= 0):

            for position in positions:

                if ((position + 1) - len(word)) >= 0:

                    for i, value in enumerate(word):

                        if value is not word_search[row - i][position - i]:
                            break

                        build_word += value

                    if word == build_word:
                        return msg.format(word, row + 1, position + 1, (row + 1) - len(word), (position + 1) - len(word))

                if (position + len(word)) <= 13:
                    for i, value in enumerate(word):

                        if value is not word_search[row - i][position + i]:
                            break

                        build_word += value

                    if word == build_word:
                        return msg.format(word, row + 1, position + 1, (row + 1) - len(word), (position + 1) + len(word))
