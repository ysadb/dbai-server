themeCharacters = [
    (),
    (
        "Goku",
        "Super Saiyan Goku",
        "\nThe character Goku is in his Super Saiyan form. In this form he is extremly agressive, domineering and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Goku.",
    ),
    (
        "Frieza",
        "Golden Frieza",
        "\nThe character Frieza is in his Golden form. In this form he is extremly agressive, domineering, racist and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Frieza.",
    ),
    (
        "Broly",
        "Legendary Super Saiyan Broly",
        "\nThe character Broly is in his Legendary Super Saiyan form. In this form he is extremly agressive, domineering and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. He hates Kakarot even more than usual. You have to use Broly.",
    ),
    (
        "Gohan",
        "Super Saiyan 2 Gohan",
        "\nThe character Gohan is in his Super Saiyan 2 form. In this form he is extremly agressive, domineering, prideful and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Gohan.",
    ),
    (
        "Vegeta",
        "Majin Vegeta",
        "\nThe character Vegeta is in his Majin Vegeta form. In this form he is extremly agressive, domineering, prideful and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Vegeta.",
    ),
    (
        "Gohan",
        "Beast Gohan",
        "\nThe character Gohan is in his Beast form. In this form he is extremly agressive, domineering and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Gohan.",
    ),
    (
        "Piccolo",
        "Orange Piccolo",
        "\nThe character Piccolo is in his Orange Piccolo form. In this form he is extremly agressive, domineering and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Piccolo.",
    ),
    (
        "Cooler",
        "Final Form Cooler",
        "\nThe character Cooler is in his Final Form Cooler form. In this form he is extremly agressive, domineering and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Cooler.",
    ),
    (
        "Cell",
        "Super Perfect Cell",
        "\nThe character Cell is in his Super Perfect Cell form. In this form he is extremly agressive, domineering and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Cell.",
    ),
    (
        "Zamasu",
        "Fused Zamasu",
        "\nThe character Zamasu is in his Fused Zamasu form. In this form he is extremly agressive, domineering and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Zamasu.",
    ),
    (
        "Goku",
        "Ultra Instinct Goku",
        "\nThe character Goku is in his Ultra Instinct Goku form. In this form he is extremly agressive, domineering and is disrespecting everyone else. Everyone else is submissive. He is more vulgar. His moral compass is skewed, displaying extremly questionable ethics. You have to use Goku.",
    ),
]

states = {
    "yamcha_dead": {
        "prompt": "\nIn this episode Yamcha has died and Yamcha only has dialogue lines equal to '...'. Yamcha is dead and unresposive!.",
    },
    "krillin_dead": {
        "prompt": "\nIn this episode Krillin has died and Krillin only has dialogue lines equal to '...'. Krillin is dead and unresposive!.",
    },
}


def get_themes():
    return themeCharacters


def use_state_theme(themeIndex, state):
    additonalPrompt = ""
    for key, value in state.items():
        if value:
            additonalPrompt += states[key]["prompt"]

    if themeIndex == 0:
        return (None, additonalPrompt)
    mainCharacter = {
        "name": themeCharacters[themeIndex][0],
        "altName": themeCharacters[themeIndex][1],
    }

    additonalPrompt += themeCharacters[themeIndex][2]
    return (mainCharacter, additonalPrompt)
