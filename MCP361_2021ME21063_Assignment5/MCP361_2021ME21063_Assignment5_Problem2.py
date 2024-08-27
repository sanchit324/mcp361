import xlrd
import salabim as sim
from scipy.stats import kstest, norm, expon
import numpy as np
from tabulate import tabulate

# Disable automatic yielding of simulation components
sim.yieldless(False)

def extract_data(sheet):
    """
    Extract non-null values for each service type from the Excel sheet.
    """
    doctor_times = []  # List to store doctor service times
    ncd_times = []     # List to store nurse service times
    pharmacist_times = []  # List to store pharmacist service times

    for row in range(1, sheet.nrows):  # Skip header row
        doctor_time = sheet.cell_value(row, 0)  # Extract doctor time from cell
        ncd_time = sheet.cell_value(row, 1)     # Extract nurse time from cell
        pharmacist_time = sheet.cell_value(row, 2)  # Extract pharmacist time from cell

        if doctor_time:  # Check if doctor time is not null
            doctor_times.append(doctor_time)  # Add time to list
        if ncd_time:  # Check if nurse time is not null
            ncd_times.append(ncd_time)  # Add time to list
        if pharmacist_time:  # Check if pharmacist time is not null
            pharmacist_times.append(pharmacist_time)  # Add time to list

    return doctor_times, ncd_times, pharmacist_times

def find_best_distribution(data):
    """
    Find the best fit distribution for the given data.
    """
    results = []  # List to store test results

    # Gaussian Distribution Test
    mean, std = norm.fit(data)  # Fit Gaussian distribution to data
    gaussian_test = kstest(data, 'norm', args=(mean, std))  # Perform KS test for Gaussian
    results.append({
        'distribution': 'Gaussian',  # Name of the distribution
        'pvalue': gaussian_test.pvalue,  # p-value from the KS test
        'parameters': {'mean': mean, 'std': std}  # Parameters of the Gaussian distribution
    })

    # Exponential Distribution Test
    loc, scale = expon.fit(data, floc=0)  # Fit Exponential distribution to data
    exponential_test = kstest(data, 'expon', args=(loc, scale))  # Perform KS test for Exponential
    results.append({
        'distribution': 'Exponential',  # Name of the distribution
        'pvalue': exponential_test.pvalue,  # p-value from the KS test
        'parameters': {'lambda': scale}  # Parameters of the Exponential distribution
    })

    # Determine best fit based on highest p-value
    best_fit = max(results, key=lambda x: x['pvalue'])  # Select the distribution with highest p-value
    return best_fit['distribution'], best_fit['parameters']  # Return the best distribution and its parameters

def print_results(name, distribution, parameters):
    """
    Print the results for the best-fit distribution.
    """
    if distribution == 'Gaussian':  # Check if the best distribution is Gaussian
        print(f"--- {name} ---")  # Print section header
        print(f"Best fit: Gaussian distribution with mean={parameters['mean']}, std={parameters['std']}")  # Print Gaussian parameters
    else:  # Otherwise, it is Exponential
        print(f"--- {name} ---")  # Print section header
        print(f"Best fit: Exponential distribution with lambda={parameters['lambda']}")  # Print Exponential parameters

class Patient(sim.Component):
    """
    Base class for patients in the system.
    """
    def process(self):
        yield self.request(nurse_service)  # Request nurse service
        yield self.hold(nurse_service_time.sample())  # Hold for nurse service time
        self.release()  # Release nurse service
        yield self.request(medical_doctor)  # Request medical doctor service
        yield self.hold(doctor_service_time.sample())  # Hold for doctor service time
        self.release()  # Release doctor service
        yield self.request(pharmacy)  # Request pharmacy service
        yield self.hold(pharmacy_service_time.sample())  # Hold for pharmacy service time
        self.release()  # Release pharmacy service

class SeniorPatient(Patient):
    """
    Class representing patients older than 30 years.
    """
    def process(self):
        yield self.request(nurse_service)  # Request nurse service
        yield self.hold(nurse_service_time.sample())  # Hold for nurse service time
        self.release()  # Release nurse service
        yield self.request(medical_doctor)  # Request medical doctor service
        yield self.hold(doctor_service_time.sample())  # Hold for doctor service time
        self.release()  # Release doctor service
        yield self.request(pharmacy)  # Request pharmacy service
        yield self.hold(pharmacy_service_time.sample())  # Hold for pharmacy service time
        self.release()  # Release pharmacy service

class JuniorPatient(Patient):
    """
    Class representing patients 30 years old or younger.
    """
    def process(self):
        yield self.request(medical_doctor)  # Request medical doctor service
        yield self.hold(doctor_service_time.sample())  # Hold for doctor service time
        self.release()  # Release doctor service
        yield self.request(pharmacy)  # Request pharmacy service
        yield self.hold(pharmacy_service_time.sample())  # Hold for pharmacy service time
        self.release()  # Release pharmacy service

def calculate_average(values):
    """
    Compute the average of a list of values.
    """
    return np.mean(values) if values else 0  # Return average, or 0 if list is empty

def configure_simulation_parameters(doctor_dist_type, doctor_dist_params, nurse_dist_type, nurse_dist_params, pharmacy_dist_type, pharmacy_dist_params):
    """
    Set up distribution parameters for the simulation.
    """
    global doctor_service_time, nurse_service_time, pharmacy_service_time
    if doctor_dist_type == 'Gaussian':  # Check if distribution type is Gaussian
        doctor_service_time = sim.Normal(doctor_dist_params['mean'], doctor_dist_params['std'])  # Set Gaussian parameters
    else:  # Otherwise, it is Exponential
        doctor_service_time = sim.Exponential(doctor_dist_params['lambda'])  # Set Exponential parameters

    if nurse_dist_type == 'Gaussian':  # Check if distribution type is Gaussian
        nurse_service_time = sim.Normal(nurse_dist_params['mean'], nurse_dist_params['std'])  # Set Gaussian parameters
    else:  # Otherwise, it is Exponential
        nurse_service_time = sim.Exponential(nurse_dist_params['lambda'])  # Set Exponential parameters

    if pharmacy_dist_type == 'Gaussian':  # Check if distribution type is Gaussian
        pharmacy_service_time = sim.Normal(pharmacy_dist_params['mean'], pharmacy_dist_params['std'])  # Set Gaussian parameters
    else:  # Otherwise, it is Exponential
        pharmacy_service_time = sim.Exponential(pharmacy_dist_params['lambda'])  # Set Exponential parameters

def execute_simulation(repetitions=1, duration=30):
    """
    Execute the simulation and gather performance data.
    """
    doctor_usage, doctor_wait_times, doctor_service_times = [], [], []  # Lists to collect doctor data
    nurse_usage, nurse_wait_times, nurse_service_times = [], [], []  # Lists to collect nurse data
    pharmacy_usage, pharmacy_wait_times, pharmacy_service_times = [], [], []  # Lists to collect pharmacy data

    for _ in range(repetitions):  # Repeat simulation
        for _ in range(duration):  # Run for specified duration
            environment = sim.Environment(trace=False, random_seed=10)  # Initialize simulation environment
            # Generate patients with specified arrival rate
            sim.ComponentGenerator(sim.Pdf((JuniorPatient, 0.4, SeniorPatient, 0.6)), iat=sim.Exponential(60 / 13), at=0, till=480)

            # Define resources with capacity
            capacity = 1
            global medical_doctor, nurse_service, pharmacy
            medical_doctor = sim.Resource("Medical Doctor", capacity=capacity)  # Create medical doctor resource
            nurse_service = sim.Resource("Nurse", capacity=capacity)  # Create nurse resource
            pharmacy = sim.Resource("Pharmacy", capacity=capacity)  # Create pharmacy resource

            environment.run()  # Run the simulation

            # Collect and store data for doctor service
            doctor_usage.append(medical_doctor.claimed_quantity.mean())
            doctor_wait_times.append(medical_doctor.requesters().length_of_stay.mean())
            doctor_service_times.append(medical_doctor.requesters().length_of_stay.mean() + medical_doctor.claimers().length_of_stay.mean())

            # Collect and store data for nurse service
            nurse_usage.append(nurse_service.claimed_quantity.mean())
            nurse_wait_times.append(nurse_service.requesters().length_of_stay.mean())
            nurse_service_times.append(nurse_service.requesters().length_of_stay.mean() + nurse_service.claimers().length_of_stay.mean())

            # Collect and store data for pharmacy service
            pharmacy_usage.append(pharmacy.claimed_quantity.mean())
            pharmacy_wait_times.append(pharmacy.requesters().length_of_stay.mean())
            pharmacy_service_times.append(pharmacy.requesters().length_of_stay.mean() + pharmacy.claimers().length_of_stay.mean())

            # Reset monitors for next simulation run
            medical_doctor.reset_monitors()
            nurse_service.reset_monitors()
            pharmacy.reset_monitors()

        environment.reset_now()  # Reset environment for next repetition

        # Calculate and return performance metrics
        avg_usage_doctor = calculate_average(doctor_usage)
        avg_wait_doctor = calculate_average(doctor_wait_times)
        avg_usage_nurse = calculate_average(nurse_usage)
        avg_wait_nurse = calculate_average(nurse_wait_times)
        avg_usage_pharmacy = calculate_average(pharmacy_usage)
        avg_wait_pharmacy = calculate_average(pharmacy_wait_times)
        avg_total_time = calculate_average(doctor_service_times) + calculate_average(nurse_service_times) + calculate_average(pharmacy_service_times)

        return {
            "avg_total_time": avg_total_time,
            "avg_wait_doctor": avg_wait_doctor,
            "avg_wait_nurse": avg_wait_nurse,
            "avg_wait_pharmacy": avg_wait_pharmacy,
            "avg_usage_doctor": avg_usage_doctor,
            "avg_usage_nurse": avg_usage_nurse,
            "avg_usage_pharmacy": avg_usage_pharmacy
        }

def display_simulation_results(metrics):
    """
    Display the simulation results in a formatted table.
    """
    headers = ["Metric", "Value"]  # Define table headers
    table_data = [  # Prepare table data
        ["Average total time in system", f"{metrics['avg_total_time']}"],
        ["Average Wait Time - Doctor", f"{metrics['avg_wait_doctor']}"],
        ["Average Wait Time - Nurse", f"{metrics['avg_wait_nurse']}"],
        ["Average Wait Time - Pharmacy", f"{metrics['avg_wait_pharmacy']}"],
        ["Utilization - Doctor", f"{metrics['avg_usage_doctor']}"],
        ["Utilization - Nurse", f"{metrics['avg_usage_nurse']}"],
        ["Utilization - Pharmacy", f"{metrics['avg_usage_pharmacy']}"]
    ]
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))  # Print the table

def main():
    # Load data from Excel file
    file_location = "Data.xls"
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)

    # Extract data
    doctor_data, nurse_data, pharmacy_data = extract_data(sheet)

    # Determine best distribution and parameters
    doctor_distribution, doctor_parameters = find_best_distribution(doctor_data)
    nurse_distribution, nurse_parameters = find_best_distribution(nurse_data)
    pharmacy_distribution, pharmacy_parameters = find_best_distribution(pharmacy_data)

    # Configure simulation parameters
    configure_simulation_parameters(
        doctor_distribution, doctor_parameters,
        nurse_distribution, nurse_parameters,
        pharmacy_distribution, pharmacy_parameters
    )

    # Execute the simulation
    results = execute_simulation(repetitions=1, duration=30)
    
    # Display results
    display_simulation_results(results)

if __name__ == "__main__":
    main()
