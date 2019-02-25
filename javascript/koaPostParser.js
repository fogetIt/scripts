const postParser = new Promise((resolve, reject) => {
    try {
        let postData = '';
        ctx.req.addListener('data', data => {
            postData += data;
        });
        ctx.req.on('end', () => {
            resolve(JSON.parse(postData));
        });
    } catch (e) {
        reject(e);
    }
})

/**
 * @usage
 * let body = {};
 * await postParser().then(jsonObj => { body = jsonObj; }).catch(console.warn);
 */