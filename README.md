# TeleLegal

<i>Make School BEW 1.2/2.2: TeleLegal</i>


## Docker Command Reference


### Build the container

```bash
docker run -p 5000:5000 --rm --name telelegal-container telelegal
```

### Remove all images with names that contain `flask`

```bash
docker images -a | grep "flask" | awk '{print $3}' | xargs docker rmi
```

### Remove all containers with names that contain `flask`

```bash
docker ps -a | grep "flask" | awk '{print $3}' | xargs docker rmi
```

### See what's running

```bash
docker ps --format '{{.Names}}'
```


## Running the Tests

**To run all of the tests**, you can run the following from the root project directory:

```
python3 -m unittest discover
```

(Make sure you have unittest installed.)

**To run all tests from a single file**, run the following:

```
python3 -m unittest telelegal_app.main.tests
```

**To run one specific test**, you can run the following:

```
python3 -m unittest telelegal_app.main.tests.MainTests.test_homepage_logged_in
```


## Deployment
View the front-end only here: https://gspuniani.github.io/TeleLegal-Winter-Intensive/. Back-end elements (such as user login authentication) are still in development.

## Purpose
TeleLegal remotely and securely connects Attorneys to Potential Clients across the State of California. Attorneys utilizing TeleLegal’s services gain access to a pool of California citizens with specific and often urgent legal questions. Either the Attorney or a Potential Client can initiate a text chat with the other as part of the initial consultation. The Attorney and Potential Client can then agree to enter a video chat to further discuss the case particulars and complete the consultation. During or after this video call, the Attorney and Potential Client--if they decide to proceed forward with the matter--may exchange additional contact information and negotiate between themselves a reasonable fee agreement. Many “routine” services, such as drafting a simple will or reviewing a standard contract, may be offered at a flat rate. Attorneys who sign up will also have access to the TeleLegal Community, a forum for lawyers to share useful practice tips with each other.

## Resources
This is a website built with the [Bootstrap v4 framework](https://getbootstrap.com). All images used in this website were freely obtained from [Unsplash](https://unsplash.com). The logo was created in [Figma](https://www.figma.com). 



