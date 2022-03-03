use std::cmp::min;
use std::{io, cmp::max};
use text_io::read;

use ndarray::{Array2, Array, ShapeBuilder, Axis};

#[derive(Clone)]
struct Node {
    children: Array2<Option<Box<Node>>>,
    state: Array2<i8>,
    won : i8,
    depth : i8,
}

fn main() {
    let mut root = Node {
        children : Array::from_elem((3, 3).f(), None),
        state : Array::zeros((3, 3).f()),
        won : 0,
        depth : 0,
    };

    build_tree(&mut root, 1);

    player_move(& root);
}

fn player_move(node : & Node) {
    let mut stdin = io::stdin();
    let input = &mut String::new();

    draw(&node.state);

    let won = check_win(&node.state);

    if won == -1 {
        println!("You have lost...");
    }
    if won == 1 {
        println!("You have won.!");
    }
    if node.depth == 9 && won == 0 {
        println!("Stalemate");
    }

    let i: usize = read!();
    println!("Read in: {}", i);

    let j: usize = read!();
    println!("Read in: {}", j);

    println!("{},{}", i, j);

    let next_move = &node.children[[ i, j]];

    match next_move {
        Some(x) => computer_move(x),
        None => return
    }

    //play();
}

fn computer_move(node : & Node) {
    for child in node.children.iter() {
        match child {
            Some(x) => {
                println!("{}", x.won);
                if x.won == -1 {
                    player_move(&x);
                    println!("found win path");
                    return;
                }
            },
            None => continue
        }
    }
    for child in node.children.iter() {
        match child {
            Some(x) => {
                if x.won == 0 {
                    player_move(&x);
                    println!("found neutral path");
                    return;
                }
            },
            None => continue
        }
    }
    for child in node.children.iter() {
        match child {
            Some(x) => {
                if x.won == 1 {
                    player_move(&x);
                    return;
                }
            },
            None => continue
        }
    }
}

fn draw(state : &Array2<i8>) {
    for i in 0..3 {
        println!(
            "|{}|{}|{}|",state[[i,0]], state[[i,1]], state[[i,2]]);
    }
}

fn build_tree(node : &mut Node, player : i8) {
    node.won = check_win(&node.state);

    if node.won != 0 || node.depth == 9 {
        return;
    }

    for i in 0..3 {
        for j in 0..3 {
            let state = node.state[[i,j]];
            
            if state != 0 {
                continue;
            }
    
            let mut new_state = node.state.clone();
            new_state[[i,j]] = player;

            let mut child = Box::new( Node {
                state : new_state,
                children : Array::from_elem((3, 3).f(), None),
                won : 0,
                depth : node.depth + 1
            });

            build_tree(&mut child, player - 2*player);
            if player == -1 {
                node.won = min(node.won, child.won);
            }
            else {
                node.won = max(node.won, child.won);
            }

            node.children[[i,j]] = Some(child);

        }
    }
}

fn check_win(state : &Array2<i8>) -> i8 {
    let mut w = state[[0,0]] + state[[0,1]] + state[[0,2]];
    w = max(state[[1,0]] + state[[1,1]] + state[[1,2]], w);
    w = max(state[[2,0]] + state[[2,1]] + state[[2,2]], w);
    w = max(state[[0,0]] + state[[1,0]] + state[[2,0]], w);
    w = max(state[[0,1]] + state[[1,1]] + state[[2,1]], w);
    w = max(state[[0,2]] + state[[1,2]] + state[[2,2]], w);
    w = max(state[[0,0]] + state[[1,1]] + state[[2,2]], w);
    w = max(state[[2,0]] + state[[1,1]] + state[[0,2]], w);

    let mut wm1= state[[0,0]] + state[[0,1]] + state[[0,2]];
    wm1 = min(state[[1,0]] + state[[1,1]] + state[[1,2]], wm1);
    wm1 = min(state[[2,0]] + state[[2,1]] + state[[2,2]], wm1);
    wm1 = min(state[[0,0]] + state[[1,0]] + state[[2,0]], wm1);
    wm1 = min(state[[0,1]] + state[[1,1]] + state[[2,1]], wm1);
    wm1 = min(state[[0,2]] + state[[1,2]] + state[[2,2]], wm1);
    wm1 = min(state[[0,0]] + state[[1,1]] + state[[2,2]], wm1);
    wm1 = min(state[[2,0]] + state[[1,1]] + state[[0,2]], wm1);

    if w == 3 {
        return 1;
    }
    if wm1 == -3 {
        return -1;
    }

    return 0;
}
