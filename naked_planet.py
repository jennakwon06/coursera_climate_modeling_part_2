import matplotlib.pyplot as plt

# Define Constants 
TIME_STEP = 100             # years
WATER_DEPTH = 4000          # meters
L = 1350                    # Watts/m2
ALBEDO = 0.3                # solar constant
EPSILON = 1                 # emissivity
SIGMA = 5.67E-8             # W/m2 K4
HEAT_CAPACITY = 1000 * 4200 * WATER_DEPTH


def create_temperature_time_plot(nSteps):

    # Initialize time, heat content, heat in & out, and heat flux lists. 
    time_list = [0]
    heat_content_list = [0]
    temperature_list = [0]
    heat_in = [L * (1 - ALBEDO) / 4]
    heat_out = [0]
    heat_flux = [(heat_in[-1] - heat_out[-1]) * 60 * 60 * 24 * 365]

    # Make N steps where each step is apart by TIME_STEP years.
    # Calculate new heat content, temperature, incoming & outgoing heat flux for every step. 
    for i in range(1, nSteps + 1):
        new_heat_content = heat_content_list[i - 1] + heat_flux[-1] * TIME_STEP
        new_temperature = new_heat_content / HEAT_CAPACITY

        outgoing_heat_flux = EPSILON * SIGMA * pow(new_temperature, 4)
        incoming_heat_flux = (L * (1 - ALBEDO)) / 4
        new_heat_flux = (incoming_heat_flux - outgoing_heat_flux) * 60 * 60 * 24 * 365

        time_list.append(time_list[i - 1] + TIME_STEP)
        heat_content_list.append(new_heat_content)
        temperature_list.append(new_temperature)
        heat_out.append(outgoing_heat_flux)
        heat_in.append(incoming_heat_flux)
        heat_flux.append(new_heat_flux)

    # Create a static plot.
    plt.plot(time_list, temperature_list)
    plt.show()


if __name__ == '__main__':
    nSteps = int(input(""))
    create_temperature_time_plot(nSteps)
