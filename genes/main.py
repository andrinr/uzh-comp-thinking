import matplotlib.pyplot as plt

def dots(a,b,W):

    if len(a) < W or len(b) < W:
        print("Invalid input")
        return

    dictA = dict()
    x = []
    y = []

    for i in range(len(a) - W):
        dictA[a[i:i+W]] = i

    for i in range(len(b) - W):
        if b[i:i+W] in dictA:
            x.append(dictA[b[i:i+W]])
            y.append(i)



    return x,y

a = "Du musst die Leute nehmen wie sind, andere gibts nicht."
b = "Du musch d Lueuet so neh wis sind, es git kei anderi."
c = "Du muesch d Luet ne wie sie sind, anderi gits net."
d = "Du muasch t Luet ne wia sie sind, andri gits nit."
e = "Du musch d Luet neh wie sie sind, anderi gits noed"
f = "je moet mensen nemen zoals ze zjin, er zjin geen anderen."
x, y = dots(e, f, 3)

fig, ax = plt.subplots()
ax.scatter(x, y)
plt.xlim([0, len(e)])
plt.ylim([0, len(f)])

plt.show()
