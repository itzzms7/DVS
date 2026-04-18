const ex = artifacts.require('Evoting')
module.exports = (dep)=>{
    dep.deploy(ex)
}