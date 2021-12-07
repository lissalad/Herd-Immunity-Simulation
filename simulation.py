import random, sys
random.seed(42)
import pytest
from person import Person
from logger import Logger
from virus import Virus


class Simulation: # RAN IMMEDIATELY
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        self.virus = virus # Virus object
        self.virus_name = virus.name
        self.pop_size = pop_size # Int
        self.initial_infected = int(initial_infected) # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.current_infected = []
        self.population = self._create_population()
        self.total_dead = 0 # Int
        self.time_step_counter = 0

        self.next_person_id = 0 # Int
        self.total_infected = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
          self.virus_name, pop_size, vacc_percentage, initial_infected)

        
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(pop_size, vacc_percentage, self.virus_name, self.virus.mortality_rate, self.virus.repro_rate)
        self.newly_infected = []

        self.alive = pop_size
        self.infected = initial_infected

  # -------------------------------------------------- #
    def run(self):
      self.time_step_counter = 0

      while self._simulation_should_continue():
        self.log_step()
        self.time_step()
      print(f'The simulation has ended after {self.time_step_counter} turns.'.format(self.time_step_counter))

# -------------------------------------------------- #
    def get_vacc_percentage(self):
      vaxxed=0
      alive=0
      for e in self.population:
        if e.is_alive:
          alive += 1
          if e.is_vaccinated:
            vaxxed += 1
      return round(vaxxed/alive, 2)

# -------------------------------------------------- #
    def log_step(self):
      vaxxed = self.get_vacc_percentage()
      print('going')
      self.logger.log_step(self.alive, self.infected,
        self.total_dead, self.time_step_counter,vaxxed)

# -------------------------------------------------- #
    def time_step(self):
      for e in self.population:
        interactions = 100
        if e.is_alive and e.infection:
          while interactions > 0:
            random_person = self.get_random_living_person(e)
            self.interaction(e, random_person)
            interactions -= 1
      self._infect_newly_infected()
      self.time_step_counter += 1
      self.newly_dead = 0

# -------------------------------------------------- #
    def interaction(self, person, random_person):
      # print(person.is_alive)
      did_infect = False
      vaxxed = False
      already_ill = None
      did_infect = None
      if random_person.is_vaccinated:
        vaxxed = True
        
      if random_person.infection:
        already_ill = True
      else:
        chance = random.uniform(0,1)
        if chance <= self.virus.repro_rate:
          did_infect = True
          self.newly_infected.append(random_person)
      # self.logger.log_interaction(person, random_person, already_ill, vaxxed, did_infect)

# -------------------------------------------------- #
    def _simulation_should_continue(self):
      if self.total_dead >= self.pop_size:
        return False
      return True

# -------------------------------------------------- #
    def _infect_newly_infected(self):
      for e in self.newly_infected:
        self.current_infected.append(e)
        e.infection = True
        self.infected += 1
        self.infected_survives(e)
      self.newly_infected = []

# -------------------------------------------------- #
    def _create_population(self):
      vaxxed = int(self.pop_size * self.vacc_percentage)
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

      for i in range(self.pop_size):
        # print(infected)
        # print(population[i].infection)
        if infected >= 1:
          if not population[i].is_vaccinated:
            population[i].infection = True
            self.current_infected.append(population[i])
            infected -= 1

      # population[0].infection = True
      return population

# -------------------------------------------------- #
    def get_random_living_person(self, e):
      random_person = random.choice(self.population)
      while random_person.is_alive==False or random_person == e: 
        random_person = random.choice(self.population)
      return random_person
      
# -------------------------------------------------- #
    def infected_survives(self, person):
      chance = random.uniform(0,1)
      if chance <= self.virus.mortality_rate:
        self.total_dead += 1
        self.alive -= 1
        person.is_alive == False
        # print(self.total_dead)
      else:
        person.is_vaccinated = True
      # self.logger.log_infection_survival(person, dead)





# -------------- RUNS --------------------- #
if __name__ == "__main__":
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


    # virus = Virus(virus_name, repro_num, mortality_rate)
    # sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    virus = Virus("Shingles", .1, .5)
    sim = Simulation(3000, 0.3, virus, 1)

    sim.run()
