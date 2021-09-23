"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[2581],{3905:function(e,a,n){n.d(a,{Zo:function(){return p},kt:function(){return h}});var t=n(7294);function r(e,a,n){return a in e?Object.defineProperty(e,a,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[a]=n,e}function o(e,a){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);a&&(t=t.filter((function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),n.push.apply(n,t)}return n}function i(e){for(var a=1;a<arguments.length;a++){var n=null!=arguments[a]?arguments[a]:{};a%2?o(Object(n),!0).forEach((function(a){r(e,a,n[a])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(n,a))}))}return e}function s(e,a){if(null==e)return{};var n,t,r=function(e,a){if(null==e)return{};var n,t,r={},o=Object.keys(e);for(t=0;t<o.length;t++)n=o[t],a.indexOf(n)>=0||(r[n]=e[n]);return r}(e,a);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(t=0;t<o.length;t++)n=o[t],a.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var l=t.createContext({}),m=function(e){var a=t.useContext(l),n=a;return e&&(n="function"==typeof e?e(a):i(i({},a),e)),n},p=function(e){var a=m(e.components);return t.createElement(l.Provider,{value:a},e.children)},c={inlineCode:"code",wrapper:function(e){var a=e.children;return t.createElement(t.Fragment,{},a)}},u=t.forwardRef((function(e,a){var n=e.components,r=e.mdxType,o=e.originalType,l=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),u=m(n),h=r,d=u["".concat(l,".").concat(h)]||u[h]||c[h]||o;return n?t.createElement(d,i(i({ref:a},p),{},{components:n})):t.createElement(d,i({ref:a},p))}));function h(e,a){var n=arguments,r=a&&a.mdxType;if("string"==typeof e||r){var o=n.length,i=new Array(o);i[0]=u;var s={};for(var l in a)hasOwnProperty.call(a,l)&&(s[l]=a[l]);s.originalType=e,s.mdxType="string"==typeof e?e:r,i[1]=s;for(var m=2;m<o;m++)i[m]=n[m];return t.createElement.apply(null,i)}return t.createElement.apply(null,n)}u.displayName="MDXCreateElement"},5952:function(e,a,n){n.r(a),n.d(a,{frontMatter:function(){return s},contentTitle:function(){return l},metadata:function(){return m},toc:function(){return p},default:function(){return u}});var t=n(7462),r=n(3366),o=(n(7294),n(3905)),i=["components"],s={},l="Block and Compositional inference",m={unversionedId:"framework_topics/programmable_inference/compositional_inference",id:"framework_topics/programmable_inference/compositional_inference",isDocsHomePage:!1,title:"Block and Compositional inference",description:"Single-site inference is not always suitable for models with highly correlated variables because, given a global assignment (or a state) in the probability distribution, changing the value of only one variable leads to a new, highly unlikely state that will rarely generate a useful sample. In other words, we may end up at a region of the posterior distribution where individual updates proposing a new value for a single random variable and deciding to accept or reject the new value (based on the Metropolis Hasting rule) are not good enough to be accepted. In these examples, however, if we change the values of a group of random variables together, we may be able to successfully change to another likely state, exploring the posterior more efficiently. Block inference allows Bean Machine to overcome the limitations of single site because highly correlated variables are updated together, allowing for states with higher probabilities.",source:"@site/../docs/framework_topics/programmable_inference/compositional_inference.md",sourceDirName:"framework_topics/programmable_inference",slug:"/framework_topics/programmable_inference/compositional_inference",permalink:"/docs/framework_topics/programmable_inference/compositional_inference",editUrl:"https://github.com/facebook/docusaurus/edit/master/website/../docs/framework_topics/programmable_inference/compositional_inference.md",tags:[],version:"current",frontMatter:{}},p=[],c={toc:p};function u(e){var a=e.components,n=(0,r.Z)(e,i);return(0,o.kt)("wrapper",(0,t.Z)({},c,n,{components:a,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"block-and-compositional-inference"},"Block and Compositional inference"),(0,o.kt)("p",null,"Single-site inference is not always suitable for models with highly correlated variables because, given a global assignment (or a ",(0,o.kt)("em",{parentName:"p"},"state"),") in the probability distribution, changing the value of only one variable leads to a new, highly unlikely state that will rarely generate a useful sample. In other words, we may end up at a region of the posterior distribution where individual updates proposing a new value for a single random variable and deciding to accept or reject the new value (based on the Metropolis Hasting rule) are not good enough to be accepted. In these examples, however, if we change the values of a group of random variables together, we may be able to successfully change to another likely state, exploring the posterior more efficiently. Block inference allows Bean Machine to overcome the limitations of single site because highly correlated variables are updated together, allowing for states with higher probabilities."),(0,o.kt)("p",null,"Referring back to the Gaussian Mixture Model (GMM), we have the following:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-py"},"@bm.random_variable\ndef alpha():\n    return dist.Dirichlet(torch.ones(K))\n\n@bm.random_variable\ndef component(i):\n    return dist.Categorical(alpha())\n\n@bm.random_variable\ndef mu(c):\n    return dist.MultivariateNormal(\n        loc=torch.zeros(2),\n        covariance_matrix=10.*torch.eye(2)\n   )\n\n@bm.random_variable\ndef sigma(c):\n    return dist.Gamma(1, 1)\n\n@bm.random_variable\ndef y(i):\n    c = component(i)\n    return dist.MultivariateNormal(\n        loc=mu(c),\n        covariance_matrix=sigma(c)**2*torch.eye(2)\n   )\n")),(0,o.kt)("p",null,"In the model above, we can either:"),(0,o.kt)("ul",null,(0,o.kt)("li",{parentName:"ul"},"Use single site inference: where we propose a new value for each random variable, and accept/reject them individually using the Metropolis Hastings rule."),(0,o.kt)("li",{parentName:"ul"},"Use block inference: where we block random variables together, sequentially propose a new value for the random variables in the block and accept/reject all proposed values together. For instance, if the proposed value of component(i), which is the component assignment for the ith data point, is to go from c to c', then y(i) is no longer a child of mu(c) and sigma(c) and is instead a child of mu(c') and sigma(c'). The likelihood of the world with the component(i)\u2018s new proposal alone is low, because, all mu(c), sigma(c), mu(c') and sigma(c') are all sampled with the assumption that y(i) was observed from component, c. Our solution here is to propose new values for mu(c), sigma(c), mu(c'), sigma(c') and component(i) and accept/reject all 5 values together.")),(0,o.kt)("p",null,"To run block inference, you can:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-py"},"mh = bm.CompositionalInference()\nmh.add_sequential_proposer([component, sigma, mu])\n\nsamples = mh.infer(queries, observations, n_samples, num_chains)\n")),(0,o.kt)("p",null,"Note that the user does not need to tell Bean Machine which ",(0,o.kt)("inlineCode",{parentName:"p"},"mu")," and ",(0,o.kt)("inlineCode",{parentName:"p"},"sigma")," need to be grouped with the component. Bean Machine only requires the random variable families to be passed to ",(0,o.kt)("inlineCode",{parentName:"p"},"add_sequential_proposer"),". The Bean Machine inference engine can then use the model dependency structure after re-sampling ",(0,o.kt)("inlineCode",{parentName:"p"},"component(i)")," from ",(0,o.kt)("span",{parentName:"p",className:"math math-inline"},(0,o.kt)("span",{parentName:"span",className:"katex"},(0,o.kt)("span",{parentName:"span",className:"katex-mathml"},(0,o.kt)("math",{parentName:"span",xmlns:"http://www.w3.org/1998/Math/MathML"},(0,o.kt)("semantics",{parentName:"math"},(0,o.kt)("mrow",{parentName:"semantics"},(0,o.kt)("mi",{parentName:"mrow"},"c")),(0,o.kt)("annotation",{parentName:"semantics",encoding:"application/x-tex"},"c")))),(0,o.kt)("span",{parentName:"span",className:"katex-html","aria-hidden":"true"},(0,o.kt)("span",{parentName:"span",className:"base"},(0,o.kt)("span",{parentName:"span",className:"strut",style:{height:"0.43056em",verticalAlign:"0em"}}),(0,o.kt)("span",{parentName:"span",className:"mord mathnormal"},"c")))))," to ",(0,o.kt)("span",{parentName:"p",className:"math math-inline"},(0,o.kt)("span",{parentName:"span",className:"katex"},(0,o.kt)("span",{parentName:"span",className:"katex-mathml"},(0,o.kt)("math",{parentName:"span",xmlns:"http://www.w3.org/1998/Math/MathML"},(0,o.kt)("semantics",{parentName:"math"},(0,o.kt)("mrow",{parentName:"semantics"},(0,o.kt)("msup",{parentName:"mrow"},(0,o.kt)("mi",{parentName:"msup"},"c"),(0,o.kt)("mo",{parentName:"msup",mathvariant:"normal",lspace:"0em",rspace:"0em"},"\u2032"))),(0,o.kt)("annotation",{parentName:"semantics",encoding:"application/x-tex"},"c'")))),(0,o.kt)("span",{parentName:"span",className:"katex-html","aria-hidden":"true"},(0,o.kt)("span",{parentName:"span",className:"base"},(0,o.kt)("span",{parentName:"span",className:"strut",style:{height:"0.751892em",verticalAlign:"0em"}}),(0,o.kt)("span",{parentName:"span",className:"mord"},(0,o.kt)("span",{parentName:"span",className:"mord mathnormal"},"c"),(0,o.kt)("span",{parentName:"span",className:"msupsub"},(0,o.kt)("span",{parentName:"span",className:"vlist-t"},(0,o.kt)("span",{parentName:"span",className:"vlist-r"},(0,o.kt)("span",{parentName:"span",className:"vlist",style:{height:"0.751892em"}},(0,o.kt)("span",{parentName:"span",style:{top:"-3.063em",marginRight:"0.05em"}},(0,o.kt)("span",{parentName:"span",className:"pstrut",style:{height:"2.7em"}}),(0,o.kt)("span",{parentName:"span",className:"sizing reset-size6 size3 mtight"},(0,o.kt)("span",{parentName:"span",className:"mord mtight"},(0,o.kt)("span",{parentName:"span",className:"mord mtight"},"\u2032")))))))))))))," to also re-sample all ",(0,o.kt)("inlineCode",{parentName:"p"},"mu")," and ",(0,o.kt)("inlineCode",{parentName:"p"},"sigma")," in old ",(0,o.kt)("inlineCode",{parentName:"p"},"component(i)"),"\u2018s Markov Blanket, ",(0,o.kt)("inlineCode",{parentName:"p"},"mu($c$)")," and ",(0,o.kt)("inlineCode",{parentName:"p"},"sigma($c$)")," and ",(0,o.kt)("inlineCode",{parentName:"p"},"mu")," and ",(0,o.kt)("inlineCode",{parentName:"p"},"sigma")," in the new Markov Blanket, ",(0,o.kt)("inlineCode",{parentName:"p"},"mu($c'$)")," and ",(0,o.kt)("inlineCode",{parentName:"p"},"sigma($c'$)"),"."))}u.isMDXComponent=!0}}]);