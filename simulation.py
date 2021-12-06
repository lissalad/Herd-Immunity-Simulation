import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation: # RAN IMMEDIATELY
    def __init__(self, pop_size, vacc_percentage, initial_infected=1, virus=""):
        self.virus_name = virus
        self.virus = virus # Virus object
        self.pop_size = pop_size # Int
        self.initial_infected = initial_infected # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.population = self._create_population()
        self.total_dead = 0 # Int

        self.next_person_id = 0 # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
          self.virus_name, pop_size, vacc_percentage, initial_infected)

        self.logger = Logger(self.file_name)
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
        print(infected)
        print(population[i].infection)
        if infected >= 1:
          if not population[i].is_vaccinated:
            population[i].infection = True
            infected -= 1

      # population[0].infection = True
      return population

# -------------------------------------------------- #
    def _simulation_should_continue(self):
      if self.total_dead == self.pop_size:
        return False
      return True

# -------------------------------------------------- #
    def run(self):
        time_step_counter = 0
        should_continue = None

        while should_continue:
          self.time_step
          should_continue = self._simulation_should_continue

        print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))

# -------------------------------------------------- #
    def time_step(self):
      for e in self.population:
        interactions = 100
        if e.is_alive and e.infection:
          while interactions > 0:
            random_person = self.get_random_person(e)
            self.interaction(e, random_person)
            interactions -= 1
      self._infect_newly_infected()
 
    def interaction(self, person, random_person):
      assert person.is_alive == True
      assert random_person.is_alive == True
      did_infect = False
      vaxxed = None
      already_ill = None
      did_infect = None
      if random_person.is_vaccinated:
        vaxxed = True
      if random_person.infection:
        already_ill = True
      else:
        chance = random.choice(0,1)
        if chance <= self.virus.repro_rate:
          did_infect = True
          self.newly_infected.append(random_person)
      self.logger.log_interaction(person, random_person, already_ill, vaxxed, did_infect)

# -------------------------------------------------- #
    def _infect_newly_infected(self):
      for e in self.newly_infected:
        e.infection = True
        e.is_alive = self.infected_survives
      self.newly_infected = []

# -------------------------------------------------- #
    def get_random_person(self, e=None):
      random_person = random.choice(self.population)
      while not random_person.is_alive: 
        while random_person == self.population[e]:
          random_person = random.choice(self.population)
      return random_person
      
# -------------------------------------------------- #
    def infected_survives(self, person):
      assert person.infection
      chance = random.choice(0,1)
      dead = False
      if chance <= self.virus.mortality_rate:
        self.total_dead += 1
        dead = True
      else:
        person.is_vaccinated = True
      self.logger.log_infection_survival(person, dead)

# -------------------------------------------------- #



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

    virus = Virus("Shingles", .2, .5)
    sim = Simulation(30, .1, 1, virus)

    sim.run()
