import pickle
import server

# layer 0: Background Objects
# layer 1: Fild Objects
# layer 2: Interactive Objects
# layer 3: Item Objects
# layer 4: Enemy Objects
# layer 5: Player Objects
objects = [[],[],[],[],[],[]]


def add_object(o, layer):
    objects[layer].append(o)


def add_objects(l, layer):
    objects[layer] += l


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break




def clear():
    for o in all_objects():
        del o
    for l in objects:
        l.clear()

def destroy():
    clear()
    objects.clear()


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

def all_layer_objects(sel):
    for o in objects[sel]:
        yield o


def save():
    with open('game.sav', 'wb') as f:
        pickle.dump(objects, f)
        pickle.dump(server.TileMap, f)

def load():
    global objects
    with open('game.sav', 'rb') as f:
        objects = pickle.load(f)
        server.TileMap = pickle.load(f)
