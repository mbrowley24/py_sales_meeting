console.log('network loaded')


const e_lan_action = document.getElementById('e-lan-action');
e_lan_action.addEventListener('click', (e)=>{

})



const drop_zone             = document.getElementById("drop-zone");

const e_lan_use_case_action = document.getElementById('e-lan-use-case-action');
const e_lan_use_case        = document.getElementById('e-lan-use-case');

const e_lan_feature_action  = document.getElementById('e-lan-feature-action');
const e_lan_feature         = document.getElementById('e-lan-feature');

const e_lan_benefit_action  = document.getElementById('e-lan-benefits-action');
const e_lan_benefit         = document.getElementById('e-lan-benefit');
const e_lan_drawing         = document.getElementById("e-lan-draw")

const fiber_container       = document.getElementById('fiber-container')

const fiber_connectors      = []

console.log(fiber_container.dataset.imagePath)
function create_images(){

    for(let i = 0; i < 20; i++){

        const img = document.createElement('img');

        img.src       = fiber_container.dataset.imagePath;
        img.alt       = "fiber"
        img.draggable = true
        img.id        = `fiber-cable-${i+1}`

        fiber_connectors.push(img);
    }


    fiber_container.append(fiber_connectors.shift());

}



drop_zone.addEventListener("drop", (e)=>{
    e.preventDefault();
    console.log('drop that shit in here')
});

e_lan_use_case_action.addEventListener('click', ()=>{

    e_lan_feature.classList.add('hide');
    e_lan_benefit.classList.add('hide');
    e_lan_use_case.classList.remove('hide');
    e_lan_use_case_action.classList.add('selected');
    e_lan_feature_action.classList.remove('selected');
    e_lan_benefit_action.classList.remove('selected');


});

e_lan_feature_action.addEventListener('click', ()=>{

    e_lan_use_case.classList.add('hide');
    e_lan_benefit.classList.add('hide');
    e_lan_feature.classList.remove('hide');
    e_lan_feature_action.classList.add('selected');
    e_lan_use_case_action.classList.remove('selected');
    e_lan_benefit_action.classList.remove('selected')
})

e_lan_benefit_action.addEventListener('click', ()=>{

    e_lan_use_case.classList.add('hide');
    e_lan_feature.classList.add('hide');
    e_lan_benefit.classList.remove('hide');
    e_lan_benefit_action.classList.add('selected');
    e_lan_use_case_action.classList.remove('selected')
    e_lan_feature_action.classList.remove('selected');
})



function elan_selection(){
    e_lan_action.classList.add('selected');
    e_lan_use_case_action.classList.add('selected');
}


elan_selection();
create_images();