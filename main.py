import os
import json
import random


class StatisticsManager:
    def __init__(self):
        self.stats_file = None
        self.stats_dir = None

    def init(self):
        self.stats_dir = "game_statistics"
        self.stats_file = os.path.join(self.stats_dir, "game_stats.json")
        self._create_directory()
        self._initialize_file()

    def _create_directory(self):

        try:
            if not os.path.exists(self.stats_dir):
                os.makedirs(self.stats_dir)
                print(f"Создана директория: {self.stats_dir}")
        except Exception as e:
            print(f"Ошибка при создании директории: {e}")

    def _initialize_file(self):

        try:
            if not os.path.exists(self.stats_file):
                default_stats = {
                    "total_games": 0,
                    "x_wins": 0,
                    "o_wins": 0,
                    "draws": 0,
                    "games": []
                }
                self._save_stats(default_stats)
                print(f"Создан файл статистики: {self.stats_file}")
        except Exception as e:
            print(f"Ошибка при создании файла статистики: {e}")

    def _load_stats(self):

        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки статистики: {e}")
            return {"total_games": 0, "x_wins": 0, "o_wins": 0, "draws": 0, "games": []}

    def _save_stats(self, stats):

        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения статистики: {e}")

    def update_statistics(self, winner, first_player):

        try:
            stats = self._load_stats()
            stats["total_games"] += 1

            if winner == "X":
                stats["x_wins"] += 1
            elif winner == "O":
                stats["o_wins"] += 1
            elif winner == "draw":
                stats["draws"] += 1


            game_info = {
                "game_number": stats["total_games"],
                "first_player": first_player,
                "winner": winner
            }
            stats["games"].append(game_info)

            self._save_stats(stats)
            print("Статистика обновлена!")

        except Exception as e:
            print(f"Ошибка обновления статистики: {e}")

    def show_statistics(self):
        """Показывает статистику"""
        try:
            stats = self._load_stats()
            print("\n" + "=" * 40)
            print("СТАТИСТИКА ИГР")
            print("=" * 40)
            print(f"Всего сыграно игр: {stats['total_games']}")
            print(f"Побед X: {stats['x_wins']}")
            print(f"Побед O: {stats['o_wins']}")
            print(f"Ничьих: {stats['draws']}")

            if stats['total_games'] > 0:
                win_rate_x = (stats['x_wins'] / stats['total_games']) * 100
                win_rate_o = (stats['o_wins'] / stats['total_games']) * 100
                draw_rate = (stats['draws'] / stats['total_games']) * 100
                print(f"\nПроцент побед X: {win_rate_x:.1f}%")
                print(f"Процент побед O: {win_rate_o:.1f}%")
                print(f"Процент ничьих: {draw_rate:.1f}%")

        except Exception as e:
            print(f"Ошибка показа статистики: {e}")


class TicTacToeGame:
    def __init__(self):
        self.stats_manager = None
        self.first_player = None
        self.current_player = None
        self.board = None

    def init(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = ""
        self.first_player = ""
        self.stats_manager = StatisticsManager()

    def print_board(self):

        print("\n   | 0 | 1 | 2 |")
        print("---------------")
        for i in range(3):
            print(f" {i} | {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]} |")
            if i < 2:
                print("---------------")

    def choose_first_player(self):

        self.first_player = random.choice(["X", "O"])
        self.current_player = self.first_player
        print(f"\nПервым ходит: {self.first_player}")

    def reset_board(self):

        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def make_move(self, row, col):

        try:
            if self.board[row][col] == " ":
                self.board[row][col] = self.current_player
                return True
            else:
                print("Эта клетка уже занята! Выберите другую.")
                return False
        except IndexError:
            print("Некорректные координаты! Используйте числа от 0 до 2.")
            return False

    def check_winner(self):

        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return row[0]


        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                return self.board[0][col]


        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]


        if all(cell != " " for row in self.board for cell in row):
            return "draw"

        return None

    def switch_player(self):

        self.current_player = "O" if self.current_player == "X" else "X"

    def get_player_input(self):

        while True:
            try:
                input_str = input(f"Игрок {self.current_player}, введите строку и столбец (0-2): ")
                coords = input_str.split()

                if len(coords) != 2:
                    print("Введите два числа через пробел! Например: '1 2'")
                    continue

                row = int(coords[0])
                col = int(coords[1])

                if row < 0 or row > 2 or col < 0 or col > 2:
                    print("Координаты должны быть от 0 до 2!")
                    continue

                return row, col

            except ValueError:
                print("Пожалуйста, введите числа!")
            except Exception as e:
                print(f"Ошибка ввода: {e}")

    def play_round(self):

        self.reset_board()
        self.choose_first_player()

        print("\n" + "=" * 50)
        print("НОВАЯ ИГРА!")
        print("=" * 50)
        print("Для хода введите два числа: номер строки и номер столбца")
        print("Например: '0 1' - первая строка, второй столбец")

        while True:
            self.print_board()


            row, col = self.get_player_input()

            if not self.make_move(row, col):
                continue

                winner: object = self.check_winner()
                if winner:
                    self.print_board()
                    if winner == "draw":
                        print("\n* Игра закончилась ничьей! *")
                    else:
                        print(f"\n* Игрок {winner} победил! *")


                    self.stats_manager.update_statistics(winner, self.first_player)
                    break


                self.switch_player()

            def main_loop(self):

                while True:
                    print("\n" + "=" * 50)
                    print("ГЛАВНОЕ МЕНЮ ")
                    print("=" * 50)
                    print("1 - Начать новую игру")
                    print("2 - Показать статистику")
                    print("3 - Выйти из игры")

                    try:
                        choice = input("\nВыберите действие (1-3): ").strip()

                        if choice == "1":
                            self.play_round()


                            while True:
                                play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower().strip()
                                if play_again in ['да', 'д', 'yes', 'y']:
                                    self.play_round()
                                elif play_again in ['нет', 'н', 'no', 'n']:
                                    break
                                else:
                                    print("Пожалуйста, введите 'да' или 'нет'")

                        elif choice == "2":
                            self.stats_manager.show_statistics()

                        elif choice == "3":
                            print("Спасибо за игру! До свидания!")
                            break

                        else:
                            print("Неверный выбор! Пожалуйста, введите 1, 2 или 3.")

                    except KeyboardInterrupt:
                        print("\n\nИгра прервана. До свидания!")
                        break
                    except Exception as e:
                        print(f"Произошла ошибка: {e}")


            if os.name == "main":
                try:
                    print("Запуск игры Крестики-нолики...")
                    game = TicTacToeGame()
                    game.main_loop()
                except Exception as e:
                    print(f"Критическая ошибка при запуске игры: {e}")

    def main_loop(self):
        pass