import random

class Fighter:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def deal_damage(self, other):
        base_damage = self.attack - other.defense
        if base_damage < 1:
            base_damage = 1
        # Add some randomness
        damage = base_damage + random.randint(-2, 2)
        if damage < 1:
            damage = 1
        other.take_damage(damage)
        return damage


def main():
    print("=== Python Fighting Game ===")
    player = Fighter("Player", health=30, attack=8, defense=3)
    enemy = Fighter("Enemy", health=25, attack=7, defense=2)

    turn = 1
    while player.is_alive() and enemy.is_alive():
        print(f"\n--- Turn {turn} ---")
        print(f"{player.name}: {player.health} HP | {enemy.name}: {enemy.health} HP")
        action = input("Choose action ([A]ttack/[Q]uit): ").strip().lower()
        if action == 'q':
            print("You fled the battle!")
            return
        elif action == 'a':
            dmg = player.deal_damage(enemy)
            print(f"You attack the enemy for {dmg} damage!")
        else:
            print("Invalid action. You lose your turn!")

        if enemy.is_alive():
            dmg = enemy.deal_damage(player)
            print(f"Enemy attacks you for {dmg} damage!")
        turn += 1

    print("\n=== Battle Result ===")
    if player.is_alive():
        print("You win!")
    else:
        print("You lose!")

if __name__ == "__main__":
    main()