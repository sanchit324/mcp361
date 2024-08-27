import xlrd  # Import the module for reading Excel files
import salabim as sim  # Import Salabim for discrete-event simulation
from scipy.stats import kstest, norm, expon  # Import statistical tests and distributions
import numpy as np  # Import NumPy for numerical operations
from tabulate import tabulate  # Import tabulate for formatted table output

# Disable automatic yielding of simulation components
sim.yieldless(False)

def extract_data(sheet):
    """
    Extract non-null values for each service type from the Excel sheet.
    """
    doctor_times = []  # List to store doctor service times
    ncd_times = []  # List to store nurse service times
    pharmacist_times = []  # List to store pharmacy service times

    for row in range(1, sheet.nrows):  # Iterate over each row in the sheet starting from the second row
        doctor_time = sheet.cell_value(row, 0)  # Get the doctor service time from the first column
        ncd_time = sheet.cell_value(row, 1)  # Get the nurse service time from the second column
        pharmacist_time = sheet.cell_value(row, 2)  # Get the pharmacy service time from the third column

        if doctor_time:  # Check if doctor_time is not null
            doctor_times.append(doctor_time)  # Add doctor_time to the list
        if ncd_time:  # Check if ncd_time is not null
            ncd_times.append(ncd_time)  # Add ncd_time to the list
        if pharmacist_time:  # Check if pharmacist_time is not null
            pharmacist_times.append(pharmacist_time)  # Add pharmacist_time to the list

    return doctor_times, ncd_times, pharmacist_times  # Return the lists of service times

def find_best_distribution(data):
    """
    Find the best fit distribution for the given data.
    """
    results = []  # List to store results of distribution tests

    # Gaussian Distribution Test
    mean, std = norm.fit(data)  # Fit Gaussian distribution to the data
    gaussian_test = kstest(data, 'norm', args=(mean, std))  # Perform Kolmogorov-Smirnov test for Gaussian fit
    results.append({
        'distribution': 'Gaussian',
        'pvalue': gaussian_test.pvalue,  # Store p-value of the Gaussian fit
        'parameters': {'mean': mean, 'std': std}  # Store parameters of the Gaussian distribution
    })

    # Exponential Distribution Test
    loc, scale = expon.fit(data, floc=0)  # Fit Exponential distribution to the data (location fixed at 0)
    exponential_test = kstest(data, 'expon', args=(loc, scale))  # Perform Kolmogorov-Smirnov test for Exponential fit
    results.append({
        'distribution': 'Exponential',
        'pvalue': exponential_test.pvalue,  # Store p-value of the Exponential fit
        'parameters': {'lambda': scale}  # Store parameter of the Exponential distribution
    })

    best_fit = max(results, key=lambda x: x['pvalue'])  # Select the distribution with the highest p-value (best fit)
    return best_fit['distribution'], best_fit['parameters']  # Return the best distribution and its parameters

def print_results(name, distribution, parameters):
    """
    Print the results for the best-fit distribution.
    """
    if distribution == 'Gaussian':  # Check if the best fit distribution is Gaussian
        print(f"--- {name} ---")  # Print section header
        print(f"Best fit: Gaussian distribution with mean={parameters['mean']}, std={parameters['std']}")
    else:  # If the best fit distribution is Exponential
        print(f"--- {name} ---")  # Print section header
        print(f"Best fit: Exponential distribution with lambda={parameters['lambda']}")

class Client(sim.Component):
    """
    Base class for clients in the system.
    """
    def process(self):
        # Simulate the sequence of requesting and releasing services
        yield self.request(nurse_service)
        yield self.hold(nurse_service_time.sample())
        self.release()
        yield self.request(medical_doctor)
        yield self.hold(doctor_service_time.sample())
        self.release()
        yield self.request(pharmacy)
        yield self.hold(pharmacy_service_time.sample())
        self.release()

class SeniorClient(Client):
    """
    Class representing clients older than 30 years.
    """
    def process(self):
        # Simulate the sequence of requesting and releasing services for senior clients
        yield self.request(nurse_service)
        yield self.hold(nurse_service_time.sample())
        self.release()
        yield self.request(medical_doctor)
        yield self.hold(doctor_service_time.sample())
        self.release()
        yield self.request(pharmacy)
        yield self.hold(pharmacy_service_time.sample())
        self.release()

class JuniorClient(Client):
    """
    Class representing clients 30 years old or younger.
    """
    def process(self):
        # Simulate the sequence of requesting and releasing services for junior clients
        yield self.request(medical_doctor)
        yield self.hold(doctor_service_time.sample())
        self.release()
        yield self.request(pharmacy)
        yield self.hold(pharmacy_service_time.sample())
        self.release()

def calculate_average(values):
    """
    Compute the average of a list of values.
    """
    return np.mean(values) if values else 0  # Return the mean of the values, or 0 if the list is empty

def calculate_std_dev(values):
    """
    Compute the standard deviation of a list of values.
    """
    return np.std(values, ddof=1) if len(values) > 1 else 0  # Return the standard deviation with Bessel's correction, or 0 if the list has 1 or fewer items

def configure_simulation_parameters(doctor_dist_type, doctor_dist_params, nurse_dist_type, nurse_dist_params, pharmacy_dist_type, pharmacy_dist_params):
    """
    Set up distribution parameters for the simulation.
    """
    global doctor_service_time, nurse_service_time, pharmacy_service_time
    # Configure the distribution for doctor service time
    if doctor_dist_type == 'Gaussian':
        doctor_service_time = sim.Normal(doctor_dist_params['mean'], doctor_dist_params['std'])
    else:
        doctor_service_time = sim.Exponential(doctor_dist_params['lambda'])

    # Configure the distribution for nurse service time
    if nurse_dist_type == 'Gaussian':
        nurse_service_time = sim.Normal(nurse_dist_params['mean'], nurse_dist_params['std'])
    else:
        nurse_service_time = sim.Exponential(nurse_dist_params['lambda'])

    # Configure the distribution for pharmacy service time
    if pharmacy_dist_type == 'Gaussian':
        pharmacy_service_time = sim.Normal(pharmacy_dist_params['mean'], pharmacy_dist_params['std'])
    else:
        pharmacy_service_time = sim.Exponential(pharmacy_dist_params['lambda'])

def execute_simulation(repetitions=1, duration=30):
    """
    Execute the simulation and gather performance data.
    """
    # Lists to store performance data for each service
    doctor_usage, doctor_wait_times, doctor_service_times = [], [], []
    nurse_usage, nurse_wait_times, nurse_service_times = [], [], []
    pharmacy_usage, pharmacy_wait_times, pharmacy_service_times = [], [], []

    for _ in range(repetitions):  # Repeat the simulation for the specified number of repetitions
        for _ in range(duration):  # Run the simulation for the specified duration
            environment = sim.Environment(trace=False, random_seed=10)  # Create a simulation environment
            sim.ComponentGenerator(sim.Pdf((JuniorClient, 0.4, SeniorClient, 0.6)), iat=sim.Exponential(60 / 13), at=0, till=480)  # Generate clients with specified arrival distribution

            capacity = 1  # Set the capacity for resources
            global medical_doctor, nurse_service, pharmacy
            medical_doctor = sim.Resource("Medical Doctor", capacity=capacity)  # Create a resource for the medical doctor
            nurse_service = sim.Resource("Nurse", capacity=capacity)  # Create a resource for the nurse
            pharmacy = sim.Resource("Pharmacy", capacity=capacity)  # Create a resource for the pharmacy

            environment.run()  # Run the simulation

            # Collect and store data for doctor service
            doctor_usage.append(medical_doctor.claimed_quantity.mean())  # Average number of doctors claimed
            doctor_wait_times.append(medical_doctor.requesters().length_of_stay.mean())  # Average wait time for doctor service
            doctor_service_times.append(medical_doctor.requesters().length_of_stay.mean() + medical_doctor.claimers().length_of_stay.mean())  # Total service time for doctor

            # Collect and store data for nurse service
            nurse_usage.append(nurse_service.claimed_quantity.mean())  # Average number of nurses claimed
            nurse_wait_times.append(nurse_service.requesters().length_of_stay.mean())  # Average wait time for nurse service
            nurse_service_times.append(nurse_service.requesters().length_of_stay.mean() + nurse_service.claimers().length_of_stay.mean())  # Total service time for nurse

            # Collect and store data for pharmacy service
            pharmacy_usage.append(pharmacy.claimed_quantity.mean())  # Average number of pharmacy claims
            pharmacy_wait_times.append(pharmacy.requesters().length_of_stay.mean())  # Average wait time for pharmacy service
            pharmacy_service_times.append(pharmacy.requesters().length_of_stay.mean() + pharmacy.claimers().length_of_stay.mean())  # Total service time for pharmacy

            # Reset monitors for next simulation run
            medical_doctor.reset_monitors()  # Reset the monitoring statistics for doctor
            nurse_service.reset_monitors()  # Reset the monitoring statistics for nurse
            pharmacy.reset_monitors()  # Reset the monitoring statistics for pharmacy

        environment.reset_now()  # Reset the environment for the next repetition

    # Calculate averages and standard deviations for performance metrics
    avg_usage_doctor = calculate_average(doctor_usage)
    avg_wait_doctor = calculate_average(doctor_wait_times)
    avg_usage_nurse = calculate_average(nurse_usage)
    avg_wait_nurse = calculate_average(nurse_wait_times)
    avg_usage_pharmacy = calculate_average(pharmacy_usage)
    avg_wait_pharmacy = calculate_average(pharmacy_wait_times)
    avg_total_time = calculate_average(doctor_service_times) + calculate_average(nurse_service_times) + calculate_average(pharmacy_service_times)

    std_dev_usage_doctor = calculate_std_dev(doctor_usage)
    std_dev_wait_doctor = calculate_std_dev(doctor_wait_times)
    std_dev_usage_nurse = calculate_std_dev(nurse_usage)
    std_dev_wait_nurse = calculate_std_dev(nurse_wait_times)
    std_dev_usage_pharmacy = calculate_std_dev(pharmacy_usage)
    std_dev_wait_pharmacy = calculate_std_dev(pharmacy_wait_times)
    std_dev_total_time = calculate_std_dev(doctor_service_times) + calculate_std_dev(nurse_service_times) + calculate_std_dev(pharmacy_service_times)

    # Return the computed metrics
    return {
        "avg_total_time": avg_total_time,
        "avg_wait_doctor": avg_wait_doctor,
        "avg_wait_nurse": avg_wait_nurse,
        "avg_wait_pharmacy": avg_wait_pharmacy,
        "avg_usage_doctor": avg_usage_doctor,
        "avg_usage_nurse": avg_usage_nurse,
        "avg_usage_pharmacy": avg_usage_pharmacy,
        "std_dev_total_time": std_dev_total_time,
        "std_dev_wait_doctor": std_dev_wait_doctor,
        "std_dev_wait_nurse": std_dev_wait_nurse,
        "std_dev_wait_pharmacy": std_dev_wait_pharmacy,
        "std_dev_usage_doctor": std_dev_usage_doctor,
        "std_dev_usage_nurse": std_dev_usage_nurse,
        "std_dev_usage_pharmacy": std_dev_usage_pharmacy
    }

def display_simulation_results(metrics):
    """
    Display the simulation results in a formatted table.
    """
    headers = ["Metric", "Mean Value", "Standard Deviation"]  # Define table headers
    table_data = [
        ["Average total time in system", f"{metrics['avg_total_time']}", f"{metrics['std_dev_total_time']}"],  # Row for average total time
        ["Average Wait Time - Doctor", f"{metrics['avg_wait_doctor']}", f"{metrics['std_dev_wait_doctor']}"],  # Row for average wait time for doctor
        ["Average Wait Time - Nurse", f"{metrics['avg_wait_nurse']}", f"{metrics['std_dev_wait_nurse']}"],  # Row for average wait time for nurse
        ["Average Wait Time - Pharmacy", f"{metrics['avg_wait_pharmacy']}", f"{metrics['std_dev_wait_pharmacy']}"],  # Row for average wait time for pharmacy
        ["Utilization - Doctor", f"{metrics['avg_usage_doctor']}", f"{metrics['std_dev_usage_doctor']}"],  # Row for doctor utilization
        ["Utilization - Nurse", f"{metrics['avg_usage_nurse']}", f"{metrics['std_dev_usage_nurse']}"],  # Row for nurse utilization
        ["Utilization - Pharmacy", f"{metrics['avg_usage_pharmacy']}", f"{metrics['std_dev_usage_pharmacy']}"]  # Row for pharmacy utilization
    ]
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))  # Print the table with pretty formatting

def main():
    # Load data from Excel file
    file_location = "Data.xls"  # Specify the path to the Excel file
    workbook = xlrd.open_workbook(file_location)  # Open the Excel workbook
    sheet = workbook.sheet_by_index(0)  # Select the first sheet in the workbook

    # Extract data
    doctor_data, nurse_data, pharmacy_data = extract_data(sheet)  # Extract service times from the sheet

    # Determine best distribution and parameters
    doctor_distribution, doctor_parameters = find_best_distribution(doctor_data)  # Find best distribution for doctor service times
    nurse_distribution, nurse_parameters = find_best_distribution(nurse_data)  # Find best distribution for nurse service times
    pharmacy_distribution, pharmacy_parameters = find_best_distribution(pharmacy_data)  # Find best distribution for pharmacy service times

    # Configure simulation parameters
    configure_simulation_parameters(
        doctor_distribution, doctor_parameters,
        nurse_distribution, nurse_parameters,
        pharmacy_distribution, pharmacy_parameters
    )

    # Execute the simulation
    results = execute_simulation(repetitions=100, duration=30)  # Run the simulation with 100 repetitions and 30 minutes duration
    
    # Display results
    display_simulation_results(results)  # Print the simulation results in a formatted table

if __name__ == "__main__":
    main()  # Execute the main function if this script is run as the main module
