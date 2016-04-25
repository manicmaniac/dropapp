appsTable = new Vue
  el: '#apps-table'
  data:
    apps: []
  filters:
    formatDate: (v)-> v.replace(/T|Z/g, ' ')
  methods:
    reload: ->
      superagent
        .get('/api/apps')
        .set('Accept', 'application/vnd.api+json')
        .end (err, res)=>
          body = res.body or JSON.parse(res.text)
          body.data.forEach (object, i)=>
            app = object.attributes
            app.id = object.id
            @apps.$set(i, app)
    remove: (event)->
      index = event.target.attributes['data-index'].value
      app = @apps[index]
      superagent
        .del("/api/apps/#{app.id}")
        .set('Accept', 'application/vnd.api+json')
        .end (err, res)=>
          @apps.$remove(app)
document.addEventListener('DOMContentLoaded', appsTable.reload)
Dropzone.options.appDropzone =
  init: ->
    @on 'success', (file, res)=>
      app = res.attributes
      app.id = res.id
      appsTable.apps.push(app)
      @removeAllFiles()
    @on 'error', (file, res)->
      file.previewElement.getElementByClassName('dz-error-message')[0].innerText = res.message
