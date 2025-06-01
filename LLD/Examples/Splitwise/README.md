# Expense Sharing CLI Application

## Description

Create a Command Line Interface (CLI) expense-sharing application. The application allows users to manage groups, add members, add expenses, simplify expenses, pay expenses, and close groups. The data for groups should be saved in a file, enabling retrieval even after reopening the application. The application should be production-grade with a CLI-based user interface.

### Features

1. **Create Group:**

   - Users can create a new expense-sharing group.

2. **Add Member:**

   - Users can add members to an existing group.

3. **Add Expense:**

   - Users can add expenses to a group with details such as payer, participants, expense type, and amount.

4. **Pay Share:**

   - Users can mark an expense as paid, updating the balances accordingly.

5. **Simplify Expenses:**

   - Users can optimize expenses within a group to minimize individual balances.

6. **Close Group:**

   - Users can close a group, finalize balances, after all payments are done.

7. **CLI Interface:**

   - The application should have a user-friendly CLI interface.
   - Options to navigate through different functionalities.
   - Clear and concise prompts for user input.

8. **Persistent Data:**

   - Save group data in a file for persistence.
   - Retrieve the data when the application is reopened.

9. **Production-Grade:**
   - The application should be robust and well-organized.
   - Follow best practices for code structure, error handling, and modularity.
   - Implement user authentication for secure group access.

### Usage

1. **CLI Commands:**

   - `create-group`: Create a new expense-sharing group.
   - `add-member`: Add a member to an existing group.
   - `add-expense`: Add an expense to a group.
   - `pay-share`: Mark an expense as paid.
   - `simplify`: Optimize expenses within a group.
   - `close-group`: Close a group and save data to a file.
   - `show`: list the expenses of a group

2. **Example Workflow:**
   - Create a group, add members, add expenses, pay expenses, simplify expenses, close the group.
