import random, sys
random.seed(42)
import pytest
from person import Person
from logger import Logger
from virus import Virus

# -------------- TO RUN --------------------- #
# python3 simulation.py ebola .25 .7 10000 ebola

class Simulation: # RAN IMMEDIATELY
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        self.virus = virus 
        self.virus_name = virus.name
        self.pop_size = pop_size 
        self.initial_infected = int(initial_infected)
        self.vacc_percentage = vacc_percentage 
        self.newly_infected = []

  # ------------------ CREATE LOGGER ------------------------- #
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
          self.virus_name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(pop_size, vacc_percentage, self.virus_name, self.virus.mortality_rate, self.virus.repro_rate)

  # ------------ COUNTS -------------------------------- #
        self.alive = pop_size
        self.dead = 0 
        self.infected = initial_infected
        self.vaxxed = initial_infected

        self.population = self._create_population()



  # -------------------------------------------------- #
    def run(self):
      self.time_step_counter = 0
      self.log_step()

      while self._simulation_should_continue():
        self.get_vacc_percentage()
        self.infected = 0
        self.time_step()
        self.log_step()


      print(f'The simulation has ended after {self.time_step_counter} turns.'.format(self.time_step_counter))
      print(f"Survivors: {self.alive}\nDead: {self.dead} ")       

# -------------------------------------------------- #
    def get_vacc_percentage(self):

      # print(living)
      # print(self.alive)
      # print(self.dead)
      # print(self.infected)
      # print(self.vaxxed)
      # print()

      percent=round(self.vaxxed/self.alive, 2)
      if percent > 1:
        percent=1.00
      self.vacc_percentage = percent

# -------------------------------------------------- #
    def log_step(self):
      # print('going')
      self.logger.log_step(self.alive, self.infected,
        self.dead, self.time_step_counter,self.vacc_percentage)

# -------------------------------------------------- #
    def time_step(self):
      for e in self.population:
        if e.is_alive and e.infection:
          interactions = 100
          while interactions > 0:
            random_person = self.get_random_living_person(e)
            self.interaction(e, random_person)
            interactions -= 1
      self._infect_newly_infected()
      self.time_step_counter += 1

# -------------------------------------------------- #
    def interaction(self, infected_person, random_person):
      # print(random_person.is_alive)
      did_infect = False
      vaxxed = False
      already_ill = None
      did_infect = None
      if random_person.is_vaccinated:
        vaxxed = True
      elif random_person.infection:
        already_ill = True
      else:
        chance = random.uniform(0,1)
        if chance <= self.virus.repro_rate:
          did_infect = True
          random_person.infection = True
          self.newly_infected.append(random_person)
      # self.logger.log_interaction(infected_person, random_person, already_ill, vaxxed, did_infect)

# -------------------------------------------------- #
    def _simulation_should_continue(self):
      if self.dead >= self.pop_size or self.vacc_percentage>=.99 or self.infected <= 0:
        return False
      return True

# -------------------------------------------------- #
    def _infect_newly_infected(self):
      for e in self.newly_infected:
        self.infected += 1
        e.infection = True
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
            self.newly_infected.append(population[i])
            infected -= 1
      # print(self.alive)
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
        self.dead += 1
        self.alive -= 1
        person.is_alive == False
        # print(self.dead)
      else:
        person.is_vaccinated = True
        self.vaxxed+=1
      # self.logger.log_infection_survival(person, dead)





# -------------- RUNS --------------------- #
if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    # virus = Virus("Shingles", .1, .5)
    # sim = Simulation(3000, 0.3, virus, 1)

    # ebola = Virus("Ebola",.7,.25)
    # sim = Simulation(10000,.9, ebola, 100)

    sim.run()

