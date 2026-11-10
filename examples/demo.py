from terminal_pet_respin import (
    add_commands,
    create_egg,
    draw_pet,
    get_stage,
    pet_says,
)


def show_pet(pet, with_message=False):

    stage = get_stage(pet["commands_run"], pet["hatch_at"])

    print(

        f"\n{pet['name']} | Commands: {pet['commands_run']} | Stage: {stage}"

    )

    if with_message:

        print(draw_pet(stage, message=pet_says(stage)))

    else:

        print(draw_pet(stage))


def main():

    print("Terminal Pet Demo")

    print("Command counts are simulated; this does not monitor your terminal.")

    pet = create_egg("Monty", hatch_at=10)

    show_pet(pet)

   
    add_commands(pet)


    show_pet(pet, with_message=True)


    for count in (4, 5, 10, 20):
        
        add_commands(pet, count)

        show_pet(pet, with_message=True)


    print("\nYou can also give your pet a custom message:")
    
    print(draw_pet(pet["stage"], message="Thanks for helping me grow!"))


if __name__ == "__main__":
    main()