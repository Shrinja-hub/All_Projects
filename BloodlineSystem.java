enum Bloodline { DRAGON, SHADOW }
 
class Ability {
    String name, description;
    int unlockLevel;
    boolean isPassive;
 
    Ability(String name, String description, int unlockLevel, boolean isPassive) {
        this.name = name;
        this.description = description;
        this.unlockLevel = unlockLevel;
        this.isPassive = isPassive;
    }
}
 
class Character {
    String name;
    Bloodline bloodline;
    int level = 1, xp = 0, xpToNext = 200;
    int strength, endurance, magic, speed, stealth;
    String[] traits;
    Ability[] abilities;
 
    Character(String name, Bloodline bloodline) {
        this.name = name;
        this.bloodline = bloodline;
        if (bloodline == Bloodline.DRAGON) {
            strength = 82; endurance = 90; magic = 65; speed = 48; stealth = 20;
            traits    = new String[]{ "Fire immunity", "Scaled skin" };
            abilities = new Ability[]{
                new Ability("Dragonfire Breath", "Cone of flame at all enemies.",      1, false),
                new Ability("Ancestral Scales",  "Reduces physical damage by 18%.",    1, true),
                new Ability("Ember Surge",       "Fire damage +40% for 3 turns.",      3, false),
                new Ability("Draconarch Form",   "Manifest dragon form for 5 turns.",  8, false),
            };
        } else {
            strength = 52; endurance = 55; magic = 78; speed = 92; stealth = 95;
            traits    = new String[]{ "Void step", "Shadow cloak" };
            abilities = new Ability[]{
                new Ability("Shadowstep",         "Teleport behind any target.",       1, false),
                new Ability("Veil Cloak",         "Stealth attacks deal 2x damage.",   1, true),
                new Ability("Soul Leech",         "Heal 30% of damage dealt.",         3, false),
                new Ability("Umbral Convergence", "Shadow rift swallows nearby foes.", 8, false),
            };
        }
    }
 
    void gainXP(int amount) {
        xp += amount;
        System.out.printf("%s gains %d XP.%n", name, amount);
        while (xp >= xpToNext) {
            xp -= xpToNext;
            level++;
            xpToNext = level * 200;
            if (bloodline == Bloodline.DRAGON) { strength += 3; endurance += 4; }
            else                               { speed    += 4; stealth   += 4; }
            System.out.printf(" Leveled up to %d! %n", level);
            for (Ability a : abilities)
                if (a.unlockLevel == level)
                    System.out.printf("  Unlocked: %s%n", a.name);
        }
    }
 
    void displayReport() {
        System.out.printf(" %s | %s | Level %d | XP %d/%d%n", name, bloodline, level, xp, xpToNext);
        System.out.printf(" STR %d  END %d  MAG %d  SPD %d  STL %d%n", strength, endurance, magic, speed, stealth);
        System.out.println(" Traits: " + String.join(", ", traits));
        System.out.println("Abilities");
        for (Ability a : abilities) {
            String tag  = a.isPassive ? "[Passive]" : "[Active] ";
            String lock = level >= a.unlockLevel ? "" : " [Lv" + a.unlockLevel + " locked]";
            System.out.printf(" %s %-22s %s%s%n", tag, a.name, a.description, lock);
        }
        System.out.println();
    }
}

public class BloodlineSystem {
        public static void main(String[] args) {
        Character dragon = new Character("Araveth Emberclaw", Bloodline.DRAGON);
        Character shadow = new Character("Nyxara Veilborne",  Bloodline.SHADOW);
 
        dragon.displayReport();
        shadow.displayReport();
 
        dragon.gainXP(900);
        System.out.println();
        dragon.displayReport();
    }
}
