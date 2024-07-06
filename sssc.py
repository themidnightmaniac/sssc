#    sssc - Simple Speed n Stuff Calculator
#    Copyright (C) 2024  Ignacio Gonsalves
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import math
import os
import sys
from tabulate import tabulate

def get_input(prompt):
    """
        Gets user input.

        Returns:
        None for empty inputs 
        A float for numbers.

        Throws an error otherwise
    """
    user_input = input(prompt)
    if user_input.strip() == "":
        return None
    try:
        return float(user_input)
    except ValueError:
        print("Invalid input. Please enter a number or leave blank.")
        return get_input(prompt)
    except KeyboardInterrupt:
        print("\nInterrupt Signal Recived, Stopping the Program...")
        sys.exit()

def run_tests():
    """
        Tests the program for both possible and impossible situations
    """

    print()
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

    print("Test Case 1: (Calculate Displacement And Time)")
    print()
    try:
        result = calculate_horizontal_motion(u=0, v=4, s=None, t=None, a=1)
        print(result)

    except ValueError as e:
        print(f"Error in Test Case 1: {e}")

    print()
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

    print("Test Case 2: (Calculate Displacement And Acceleration)")
    print()
    try:
        result = calculate_horizontal_motion(u=0, v=4, s=None, t=4.0, a=None)
        print(result)

    except ValueError as e:
        print(f"Error in Test Case 2: {e}")

    print()
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

    print("Test Case 3: (Calculate Displacement And Acceleration On Constant Velocity)")
    print()
    try:
        result = calculate_horizontal_motion(u=4, v=4, s=None, t=4.0, a=None)
        print(result)

    except ValueError as e:
        print(f"Error in Test Case 3: {e}")

    print()
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

    print("Test Case 4 - Physically Impossible: (Calculate Time On Constant Velocity)")
    print()
    try:
        result = calculate_horizontal_motion(u=10, v=10, s=10, t=None, a=0)
        print(result)

    except ValueError as e:
        print(f"Error in Test Case 4: {e}")

    print()
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

    print("Test Case 5 - Physically Impossible: (Calculate Time And Acceleration While Stationary)")
    print()
    try:
        result = calculate_horizontal_motion(u=0, v=0, s=10, t=None, a=None)
        print(result)

    except ValueError as e:
        print(f"Error in Test Case 5: {e}")

    print()
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

    print("Test Case 6 : (Calculate Deceleration And Displacement)")
    print()
    try:
        result = calculate_horizontal_motion(u=4, v=0, s=None, t=4.0, a=None)
        print(result)

    except ValueError as e:
        print(f"Error in Test Case 6: {e}")

    print()
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

    print("Test Case 7 : (All Values Already Provided)")
    print()
    try:
        result = calculate_horizontal_motion(u=0, v=4, s=8, t=4.0, a=1.0)
        print(result)

    except ValueError as e:
        print(f"Error in Test Case 7: {e}")

    print()
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

def calculate_horizontal_motion(u=None, v=None, s=None, t=None, a=None):
    """
    Calculates the unknown horizontal motion parameters using kinematic equations.
    
    Parameters:
    u (float): Initial velocity (u)
    v (float): Final velocity (v)
    s (float): Displacement (s)
    t (float): Time (t)
    a (float): Acceleration (a)
    
    Returns:
    A dictionary containing all five parameters with calculated values where necessary.
    """

    # Check physically impossible conditions
    if u == 0 and v == 0 and s != 0:
        raise ValueError("Physically impossible condition: both velocities are zero but displacement is non-zero.")

    if a == 0 and u != v:
        raise ValueError("Physically impossible condition: acceleration is zero but velocity changed.")

    if a != 0 and a is not None and u == v:
        raise ValueError("Physically impossible condition: acceleration is non zero but velocity is constant.")

    for _ in range(2):  # Loop twice to resolve interdependencies
        if u is not None and v is not None and t is not None:
            a = (v - u) / t
            s = u * t + 0.5 * a * t**2

        elif u is not None and v is not None and s is not None:
            if a == 0 and t is None:
                raise ValueError("Cannot calculate time when acceleration is zero (constant velocity).")
            a = (v**2 - u**2) / (2 * s)
            if t is None:
                if a == 0:
                    raise ValueError("Cannot calculate time when acceleration is zero (constant velocity).")
                t = (v - u) / a

        elif u is not None and s is not None and t is not None:
            if t == 0:
                raise ValueError("Time cannot be zero.")
            a = (2 * (s - u * t)) / t**2
            v = u + a * t

        elif v is not None and s is not None and t is not None:
            if t == 0:
                raise ValueError("Time cannot be zero.")
            a = (2 * (s - v * t)) / t**2
            u = v - a * t

        elif u is not None and v is not None and a is not None:
            if a == 0 and t is None:
                raise ValueError("Cannot calculate time when acceleration is zero (constant velocity).")
            s = (v**2 - u**2) / (2 * a)
            if t is None:
                if a == 0:
                    raise ValueError("Cannot calculate time when acceleration is zero (constant velocity).")
                t = (v - u) / a

        elif u is not None and s is not None and a is not None:
            if a == 0 and t is None:
                raise ValueError("Cannot calculate time when acceleration is zero (constant velocity).")
            v = math.sqrt(u**2 + 2 * a * s)
            if t is None:
                if a == 0:
                    raise ValueError("Cannot calculate time when acceleration is zero (constant velocity).")
                t = (v - u) / a

        elif v is not None and s is not None and a is not None:
            if a == 0 and t is None:
                raise ValueError("Cannot calculate time when acceleration is zero (constant velocity).")
            u = math.sqrt(v**2 - 2 * a * s)
            if t is None:
                if a == 0:
                    raise ValueError("Cannot calculate time when acceleration is zero (constant velocity).")
                t = (v - u) / a

        elif u is not None and t is not None and a is not None:
            if t == 0:
                raise ValueError("Time cannot be zero.")
            v = u + a * t
            s = u * t + 0.5 * a * t**2

        elif v is not None and t is not None and a is not None:
            if t == 0:
                raise ValueError("Time cannot be zero.")
            u = v - a * t
            s = u * t + 0.5 * a * t**2

        elif s is not None and t is not None and a is not None:
            if t == 0:
                raise ValueError("Time cannot be zero.")
            u = (s - 0.5 * a * t**2) / t
            v = u + a * t

        elif u is not None and v is not None:
            if a == 0 and t is None:
                raise ValueError("Cannot calculate time when acceleration is zero (constant velocity).")
            if t is None:
                t = (v - u) / a
            s = u * t + 0.5 * a * t**2

        elif u is not None and t is not None:
            if t == 0:
                raise ValueError("Time cannot be zero.")
            v = u + a * t
            s = u * t + 0.5 * a * t**2

        elif v is not None and t is not None:
            if t == 0:
                raise ValueError("Time cannot be zero.")
            u = v - a * t
            s = u * t + 0.5 * a * t**2

    return {
        "Initial Velocity (m/s)": u,
        "Final Velocity (m/s)": v,
        "Displacement (m)": s,
        "Time (s)": t,
        "Acceleration (m/s²)": a
    }

def calculate_vertical_motion(u=None, v=None, s=None, t=None, a=None):
    """
    Calculates the unknown vertical motion parameters using kinematic equations with given acceleration.

    Parameters:
    u (float): Initial vertical velocity (m/s)
    v (float): Final vertical velocity (m/s)
    s (float): Vertical displacement (m)
    t (float): Time (s)
    a (float): Acceleration (m/s²), assumed constant (e.g., due to gravity)
    
    Returns:
    A dictionary containing all parameters with calculated values where necessary.
    """
    # Check if vertical acceleration is provided, if not, assume gravity
    if a is None:
        a = 9.81  # default gravity in m/s^2

    # Check if vertical initial velocity is provided, if not, assume freefall
    if u is None:
        u = 0  # default gravity in m/s^2

    # Count the number of provided (non-None) parameters
    params = [u, v, s, t]
    known_params_count = len([p for p in params if p is not None])

    if known_params_count < 1:
        raise ValueError("At least one parameters must be provided.")

    # Using kinematic equations to find missing values
    for _ in range(2):  # Loop twice to ensure interdependencies are resolved
        if u is not None and v is not None and t is not None:
            s = u * t + 0.5 * a * t**2
        elif u is not None and v is not None and s is not None:
            t = (v - u) / a
        elif u is not None and s is not None and t is None:
            t = math.sqrt(2 * s / a)
            v = u + a * t
        elif v is not None and s is not None and t is None:
            t = (v - u) / a
        elif u is not None and v is not None:
            s = (v**2 - u**2) / (2 * a)
        elif u is not None and s is not None:
            v = math.sqrt(u**2 + 2 * a * s)
        elif v is not None and s is not None:
            u = math.sqrt(v**2 - 2 * a * s)
        elif u is not None and t is not None:
            v = u + a * t
        elif v is not None and t is not None:
            u = v - a * t
        elif s is not None and t is not None:
            t = math.sqrt(2 * s / a)
            u = (s - 0.5 * a * t**2) / t
            v = u + a * t
        elif t is not None:
            s = 0.5 * a * t**2

    return {
        "Initial Vertical Velocity (m/s)": u,
        "Final Vertical Velocity (m/s)": v,
        "Vertical Displacement (m)": s,
        "Time (s)": t,
        "Acceleration (m/s²)": a
    }

def calculate_vector_properties(horiz_motion, vert_motion):
    """
    Calculates the direction (angle) and modulus (magnitude) of the velocity vector 
    based on final horizontal and vertical velocities.
    
    Parameters:
    horizontal_motion (dict): Dictionary containing horizontal motion parameters.
    vertical_motion (dict): Dictionary containing vertical motion parameters.
    
    Returns:
    A dictionary containing the direction (angle) and the modulus (magnitude) of the velocity vector.
    """
    # Extract final velocities
    horiz_velocity = horiz_motion.get("Final Velocity (m/s)", 0)
    vert_velocity = vert_motion.get("Final Vertical Velocity (m/s)", 0)

    # Calculate the modulus (magnitude) of the resultant velocity vector
    velocity_magnitude = math.sqrt(horiz_velocity**2 + vert_velocity**2)

    # Calculate the angle (θ) in degrees based on final velocities
    angle = math.degrees(math.atan2(vert_velocity, horiz_velocity))

    return {
        "Velocity Vector Direction (deg)": angle,
        "Velocity Vector Modulus (m/s)": velocity_magnitude
    }

#Clear Terminal
os.system('clear')

# Ask the user for the desired type of movement.
try:
    choice = int(input("Choose the type of movement:\n1) Horizontal Linear Accelerated\n2) Vertical Linear Accelerated\n3) Both\n4) Run Tests\nChoice: "))
    lista = (1, 2, 3, 4)
    if choice not in lista:
        raise ValueError("Please Choose An Available Option.")
except ValueError as err:
    print("Error: ", err)
except KeyboardInterrupt:
    print("\nInterrupt Signal Recived, Stopping the Program...")
    sys.exit()

# Ask the user for the required values based on his choice.
try:
    if choice == 1:

        #Clear Terminal
        os.system('clear')

        # Horizontal
        print("Enter values for horizontal motion (leave blank if unknown):")
        horiz_init_velocity = get_input("Initial Horizontal Velocity (m/s): ")
        horiz_final_velocity = get_input("Final Horizontal Velocity (m/s): ")
        horiz_displacement = get_input("Horizontal Displacement (m): ")
        horiz_time = get_input("Time (s): ")
        horiz_acceleration = get_input("Horizontal Acceleration (m/s²): ")

        horiz_result = calculate_horizontal_motion(horiz_init_velocity, horiz_final_velocity, horiz_displacement, horiz_time, horiz_acceleration)

        horiz_table = tabulate(horiz_result.items(), headers=["Parameter", "Value"], tablefmt="grid")

        os.system('clear')

        print("Horizontal Vector")
        print(horiz_table)
        print("")

    elif choice == 2:

        #Clear Terminal
        os.system('clear')

        # Vertical
        print("Enter values for vertical motion (leave blank if unknown):")
        vert_init_velocity = get_input("Initial Vertical Velocity (m/s): ")
        vert_final_velocity = get_input("Final Vertical Velocity (m/s): ")
        vert_displacement = get_input("Vertical Displacement (m): ")
        vert_time = get_input("Time (s): ")

        vert_result = calculate_vertical_motion(vert_init_velocity, vert_final_velocity, vert_displacement, vert_time)

        vert_table = tabulate(vert_result.items(), headers=["Parameter", "Value"], tablefmt="grid")

        os.system('clear')

        print("Vertical Vector")
        print(vert_table)
        print("")

    elif choice == 3:

        #Clear Terminal
        os.system('clear')

        # Horizontal
        print("Enter values for horizontal motion (leave blank if unknown):")
        horiz_init_velocity = get_input("Initial Velocity (m/s): ")
        horiz_final_velocity = get_input("Final Velocity (m/s): ")
        horiz_displacement = get_input("Displacement (m): ")
        horiz_time = get_input("Time (s): ")
        horiz_acceleration = get_input("Acceleration (m/s²): ")
        # Vertical
        print("Enter values for vertical motion (leave blank if unknown):")
        vert_init_velocity = get_input("Initial Vertical Velocity (m/s): ")
        vert_final_velocity = get_input("Final Vertical Velocity (m/s): ")
        vert_displacement = get_input("Vertical Displacement (m): ")
        vert_time = get_input("Time (s): ")

        vert_result = calculate_vertical_motion(vert_init_velocity, vert_final_velocity, vert_displacement, vert_time)
        horiz_result = calculate_horizontal_motion(horiz_init_velocity, horiz_final_velocity, horiz_displacement, horiz_time, horiz_acceleration)
        vector_properties = calculate_vector_properties(horiz_result, vert_result)

        horiz_table = tabulate(horiz_result.items(), headers=["Parameter", "Value"], tablefmt="grid")
        vert_table = tabulate(vert_result.items(), headers=["Parameter", "Value"], tablefmt="grid")
        vector_table = tabulate(vector_properties.items(), headers=["Parameter", "Value"], tablefmt="grid")

        os.system('clear')

        print("Horizontal Vector")
        print(horiz_table)
        print("")
        print("Vertical Vector")
        print(vert_table)
        print("")
        print("Combined Velocity Vector Properties")
        print(vector_table)

    elif choice == 4:

        #Clear Terminal
        os.system('clear')

        run_tests()
except ValueError as err:
    print(err)
except KeyboardInterrupt:
    print("\nInterrupt Signal Recived, Stopping the Program...")
    sys.exit()
