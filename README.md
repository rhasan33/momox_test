# Momox Coding Challenge

## Prerequisites

- The follwoing things need to installed to run the project

  - `docker`
  - `docker-compose`

- In the `src` folder need to replace the data of `employee_orders.xml` and `menu.json` files.
- **The files' name and data format cannot be changed. Otherwise the expected output will not come**

## How to run

In order to run the project, needed to change the directory to project path and run `docker-compose run app`.

Sample:

- `cd to/the/project/directory`
- `docker-compose run app`

If one need to check with different data format, just need to change the data of above mentioned files and run `docker-compose run app` again

## Output

If everything goes fine, then `'order created'` will be shown in the terminal and `orders.json` file will be created in the `src` folder. `orders.json` holds the json data, with that the bulk create order request can be done.

In the codebase, it is also commented that what if the requests fails and how to handle those.

Again, if there is any error, that will be shown in the terminal as well.
