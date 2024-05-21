class Ordi:

  def __init__(self, id_, connected_to, ordis):
  
    self.ordis = ordis
  
    self.id_ = id_
    
    self.connected_to = connected_to
    
    self.weights = []
    
    self.sum_weights = 0
  
  def connect_to(self, indx):
  
    self.connected_to.append(indx)

    if len(self.connected_to) > 1:
    
      return 1
   
  def init_weights(self, asking_for=-1):
  
    if len(self.connected_to) == 1:
    
      self.weights = 1
    
    else:
    
      for co_ordi in self.connected_to:
      
        if not co_ordi == asking_for:

          #print(co_ordi, len(self.ordis))

          self.ordis[co_ordi].init_weights(asking_for=self.id_)
      
          self.weights.append(self.ordis[co_ordi].sum_weights+1)
      
      if asking_for != -1:
      
        self.sum_weights = sum(self.weights)
        
        self.weights.append(len(self.ordis)-self.sum_weights-1)#self.weights[self.connected_to.index(asking_for)] = len(self.ordis) - self.sum_weights
      

def ordi_weight(ordi):

  if ordi.weights != 1:
  
    return max(ordi.weights)

  else:

    return 100001


def main():

  nb_ordis = int(input())

  ordis = [Ordi(x, [], []) for x in range(nb_ordis)]
  
  starting = None
  
  for x in range(nb_ordis-1):
  
    indx1, indx2 = list(map(int, input().split()))
    
    if ordis[indx1].connect_to(indx2):
    
      starting  = indx1
    
    else:
    
      ordis[indx1].ordis = ordis
    
    if ordis[indx2].connect_to(indx1):
    
      starting  = indx2
     
    else:
    
      ordis[indx2].ordis = ordis
  
  # all computers being linked, initialisating one will do the job (for all)
  ordis[starting].init_weights()
  
  print(max(min(ordis, key=ordi_weight).weights))


main()
