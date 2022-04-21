# League Manager
League Manager is a Python project using PyQT5 interface.

## Description
League Manager allows the user to create leagues, which contains teams, and team members. It also allows the user to load and save a League instance. As well as importing and exporting teams. The interface has the ability to add, delete, and edit the above.

## How To
### Start
Go to the Final Project directory and enter:
```
python -m league_manager.pyqt5.logic.main_window
```
This should open the Main Window of the application. 

### Main Window
The main window opens League Manager. At the menu bar, you have the option to load an instance of the league manager, save an instance, or quit. 

You can also type in the name of the league you would like to add, and click on the "Add" button. 

Once a league is added, it will show up on the list, which you can then edit or delete.
![Alt text](images/main_window.png?raw=true "Main Window")

### League Editor
Upon selecting a specific league to edit in the main window, it will pop up a modal League Editor window.

Here all the teams that are in that league are listed. You have the option to add, edit, or delete teams in this league.

You have the option to import a CSV file with the team name, member name, and member emails. You can also export it into a CSV file. 
![Alt text](images/league_editor.png?raw=true "League Editor")
### Team Editor
Upon selecting a specific team to edit in the league editor, it will pop up a modal Team Editor window.

Here all the members that are in that team are listed. You have the option to add, edit, or delete member in this team.
![Alt text](images/team_editor.png?raw=true "Team Editor")

To update a team member, select the member, and click "Update". The form on the top will change to the information of the member you selected. Once the changes are done, click "Confirm". 
![Alt text](images/update_member.png?raw=true "Team Editor")

## Author
Jin Hu