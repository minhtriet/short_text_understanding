(this.webpackJsonpshort_text_understand=this.webpackJsonpshort_text_understand||[]).push([[0],[,,,,,,,,function(e,t,n){e.exports=n(9)},function(e,t,n){"use strict";n.r(t);var a=n(2),r=n(3),u=n(1),o=n(6),c=n(5),i=n(0),s=n.n(i),l=n(4),h=n.n(l),d=(n(14),n(15),n(16),s.a.createElement),p=function(e){Object(o.a)(n,e);var t=Object(c.a)(n);function n(e){var r;return Object(a.a)(this,n),(r=t.call(this,e)).state={query:""},r.handleChange=r.handleChange.bind(Object(u.a)(r)),r.handleSubmit=r.handleSubmit.bind(Object(u.a)(r)),r}return Object(r.a)(n,[{key:"handleSubmit",value:function(e){var t=this;window.history.pushState("","","api/v1/query=".concat(this.state.query)),fetch("{process.env.REACT_APP_SERVER_URL}/api/v1?query=".concat(encodeURIComponent(this.state.query))).then((function(e){return e.json()})).then((function(e){var n=[];if("error"in e)n.push(e.error);else for(var a=0,r=0;r<t.state.query.length;)a>=e.length||r!==e[a].start_pos?(n.push(t.state.query.charAt(r)),r++):(r=e[a].end_pos+1,n.push(d("a",{href:"".concat("https://www.wikidata.org/wiki/").concat(e[a].name),key:a},t.state.query.slice(e[a].start_pos,e[a].end_pos))),n.push(d("div",{className:"footnote",key:"".concat(a,"_fn")}," (".concat(e[a].description,") "))),a+=1);h.a.render(n,document.getElementById("result"))}),(function(e){console.log(e)})),e.preventDefault()}},{key:"handleChange",value:function(e){this.setState({query:e.target.value})}},{key:"render",value:function(){return s.a.createElement("div",null,s.a.createElement("form",{onSubmit:this.handleSubmit,method:"GET"},s.a.createElement("input",{id:"textbox_query",value:this.state.query,onChange:this.handleChange,type:"text",autoFocus:!0})),s.a.createElement("div",{id:"result"}))}}]),n}(s.a.Component),m=function(e){Object(o.a)(n,e);var t=Object(c.a)(n);function n(){return Object(a.a)(this,n),t.apply(this,arguments)}return Object(r.a)(n,[{key:"render",value:function(){return s.a.createElement("div",null,s.a.createElement("h1",null,"nerd"),s.a.createElement(p,null))}}]),n}(s.a.Component);h.a.render(s.a.createElement(m,null),document.getElementById("root"))},,,,,function(e,t,n){},function(e,t,n){},function(e,t,n){}],[[8,1,2]]]);
//# sourceMappingURL=main.84b89e35.chunk.js.map