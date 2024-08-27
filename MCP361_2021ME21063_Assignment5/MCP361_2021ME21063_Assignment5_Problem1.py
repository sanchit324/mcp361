import xlrd
from scipy.stats import kstest, norm, expon
from tabulate import tabulate

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
             
def main():
    # Load the Excel file and sheet
    loc = "Data.xls"
    workbook = xlrd.open_workbook(loc)
    sheet = workbook.sheet_by_index(0)

    # Extract data
    doctor_times, ncd_times, pharmacist_times = extract_data(sheet)

    # Test and display results for each service type
    doctor_dist, doctor_params = find_best_distribution(doctor_times)
    nurse_dist, nurse_params = find_best_distribution(ncd_times)
    pharmacist_dist, pharmacist_params = find_best_distribution(pharmacist_times)

    # Print results
    print_results('Doctor', doctor_dist, doctor_params)
    print_results('NCD Nurse', nurse_dist, nurse_params)
    print_results('Pharmacist', pharmacist_dist, pharmacist_params)

if __name__ == "__main__":
    main()
