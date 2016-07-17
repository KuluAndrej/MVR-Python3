models = open('/home/kuluandrej/Ipython3_notebook_projects/MVR_py/data/init_models.txt', 'r').readlines()
models = list(map(lambda x: x.strip(), models))
print(models)