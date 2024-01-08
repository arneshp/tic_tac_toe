import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

game_state = [""] * 9
player_turn = "X"

def check_winner(game_state):
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for combo in winning_combinations:
        if game_state[combo[0]] == game_state[combo[1]] == game_state[combo[2]] != "":
            return game_state[combo[0]]
    if "" not in game_state:
        return "Draw"
    return None

app.layout = html.Div(
    [
        html.H1("Tic Tac Toe"),
        html.Div(id="game_board",
                 children=[html.Button(id=f"cell-{idx}", n_clicks=0,style= {'width': '25%','height': '50px','marginBottom': 50, 'marginTop': 25}) for idx in range(0,3)]),
        html.Div(id="game_board",
                 children=[html.Button(id=f"cell-{idx}", n_clicks=0,style= {'width': '25%','height': '50px','marginBottom': 50, 'marginTop': 25}) for idx in range(3,6)]),         
        html.Div(id="game_board",
                 children=[html.Button(id=f"cell-{idx}", n_clicks=0,style= {'width': '25%','height': '50px','marginBottom': 50, 'marginTop': 25}) for idx in range(6,9)]),

        html.Button('Reset', id='reset_button'),
        html.Div(id='winner'),
    ]
)

@app.callback(
    [Output(f"cell-{idx}", "children") for idx in range(9)] +
    [Output('winner', 'children')],
    [Input(f"cell-{idx}", "n_clicks") for idx in range(9)] +
    [Input('reset_button', 'n_clicks')],
    [State(f"cell-{idx}", "children") for idx in range(9)]
)
def tic_tac_toe(*args):
    global game_state, player_turn
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if "reset" in button_id:
        game_state = [""] * 9
        player_turn = "X"
    elif "cell" in button_id:
        idx = int(button_id.split("-")[1])
        if game_state[idx] == "":
            game_state[idx] = player_turn
            player_turn = "O" if player_turn == "X" else "X"
    winner = check_winner(game_state)
    return game_state + ([f"Player {winner} wins!"] if winner else [""])

if __name__ == '__main__':
    app.run_server(debug=True)