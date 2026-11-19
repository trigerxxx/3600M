# Ролик №2: Everest — 44 Days in the Dark (длинный формат)

Длина 8:14, 1920×1080, английский рассказчик, субтитры, звуковой дизайн. История автора про Ильяса, поворот с 52-м днём. Ролик подводит к игре «EVEREST: Get Down Alive».

Видео в репозиторий не кладём: файл больше 100 МБ, такие GitHub не принимает. Чтобы собрать заново: `python3 source/render.py`.

## Что внутри
- 6 глав + вступление, 53 части, 23 вида сцен (low-poly: холодный синий снаружи, тёплый оранжевый внутри, красный для опасности).
- Звук полностью синтезирован кодом, поэтому проблем с правами нет: ветер, шторм, хлопки палатки, шаги по снегу, дыхание, сердце, разрыв ткани, иголка, молния палатки, рация с голосом «Ilyas, do you copy?», шёпот, гудки трекера, удары, музыка под настроение (тьма, тревога, надежда). Музыка приглушается под голос.
- Громкость −14 LUFS (норма YouTube).

## Для YouTube
**Название:** He Survived 44 Days on Everest. Then He Checked the Date.

**Описание:**
A climber is trapped above 8,000 meters after a storm. The search is called off. The world thinks he's dead. He has two rules, a knife, a flask, and a tracker counting down to the weather window. 44 days. Or so he thought.

This is a fictional story.

Chapters:
0:00 Intro
0:49 Chapter 1: The Storm
2:02 Chapter 2: The Rules
3:06 Chapter 3: The Long Dark
4:30 Chapter 4: Day 41
5:44 Chapter 5: Day 44
6:35 Chapter 6: The Mistake

How many days would you last? Tell me in the comments.

**Отметки:** загрузить everest.srt как субтитры (English). В «Изменённый или синтетический контент» — нет (анимация, не реалистичное видео). Аудитория — не «для детей».

## Что улучшить
- Голос: ElevenLabs, голос Brian (`source/el_tts.py`). Ключ хранится в настройках окружения, не в коде. Рация — George, шёпот — Sarah.
- Сделать 3–4 Shorts из лучших моментов (52-й день, разрыв палатки, тень у палатки) со ссылкой на длинное видео.

## Shorts (9:16, `source/shorts.py`)
| Файл | Длина | Крючок сверху |
|---|---|---|
| short1-day52 | 55 с | HE COUNTED 44 DAYS ON EVEREST |
| short2-tear | 58 с | DAY 41. MINUS 40. THE TENT RIPS. |
| short3-shadow | 30 с | SOMEONE WAS OUTSIDE HIS TENT. AT 8,000 M. |

Как выкладывать: длинное видео первым, затем по одному Shorts в день. В YouTube Studio у каждого Shorts в поле «Связанное видео» выбрать длинный ролик, тогда под Shorts появится кнопка перехода на него.
Названия: «He counted 44 days on Everest… he was wrong #shorts», «His tent ripped at -40° #shorts», «Someone was outside his tent at 8,000 m #shorts».
