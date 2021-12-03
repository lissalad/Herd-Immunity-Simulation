import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation: # RAN IMMEDIATELY
    def __init__(self, pop_size, vacc_percentage, initial_infected=1, virus=""):
        # ------------------------ #
        self.virus_name = virus
       # ------------------------ #
        self.logger = None
        self.pop_size = pop_size # Int

        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.population = self._create_population()

        self.logger = Logger("cool")
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
          self.virus_name, pop_size, vacc_percentage, initial_infected)
        self.newly_infected = [] # ???

    def _create_population(self):
      vaxxed = self.pop_size * self.vacc_percentage
      infected = self.initial_infected
      population = []
      counter = self.pop_size
      for i in range(self.pop_size):
        if vaxxed > 0:
          person = Person(counter,True)
          population.append(person)
          vaxxed -= 1
        else:
          person = Person(counter,False)
          population.append(person)

        counter -= 1

      counter = 0
      while infected > 0:
        if(not population[counter].is_vaccinated):
          population[counter].infection = True
          infected -= 1
      return population


      
    def _simulation_should_continue(self):
      pass

    def run(self):
        time_step_counter = 0
        should_continue = None

        while should_continue:
          print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))

    def time_step(self):
      self._infect_newly_infected()
      self.newly_infected = []

    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True

        pass

    def _infect_newly_infected(self):
        
        pass

# -------------- RUNS --------------------- #
# if __name__ == "__main__":
    # params = sys.argv[1:]
    # virus_name = str(params[0])
    # repro_num = float(params[1])
    # mortality_rate = float(params[2])

    # pop_size = int(params[3])
    # vacc_percentage = float(params[4])

    # if len(params) == 6:
    #     initial_infected = int(params[5])
    # else:
    #     initial_infected = 1

    # virus = Virus(name, repro_rate, mortality_rate)
    # sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    # sim.run()
