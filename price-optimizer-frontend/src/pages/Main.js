import React from 'react';

import './Main.css'

export default function Main() {
    return (
        <div className="container bg-light p-4">
            <div className="mainPageTitleBlock row d-flex flex-column align-itens center justify-content-center text-center shadow p-4">
                <h1 className="mainPageTitle"> MTG Price Optimizer </h1> 
                <h3 className="text-white"> Aqui tem que ir uma descrição do que fazer </h3>
            </div>
            <div className="row d-flex mt-4">
                <div className="formInsertCards d-flex flex-column shadow justify-content-center align-itens-center p-4 m-2 col">
                    <div className="d-flex justify-content-center">
                        <div class="group">
                            <input type="text" required="required"/>
                            <span class="highlight"></span>
                            <span class="bar"></span>
                            <label>Quantidade e nome da carta</label>
                        </div>
                    </div>
                    <button className="insertCardButton mx-auto w-75 p-2"> INSERIR NA LISTA </button>
                </div>
                <div className="formInsertCards resultListCards shadow p-4 m-2 col">
                    
                </div>
            </div>
        </div>
    );
}